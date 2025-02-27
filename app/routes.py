from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import os
from werkzeug.utils import secure_filename
from app.services.template_validator import TemplateValidator
from app.services.script_generator import ScriptGenerator
from app.services.time_tracker import TimeTracker
from datetime import datetime, timedelta
import pandas as pd

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {
    'template': {'txt'},
    'data': {'xlsx', 'xls'}
}

def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

def cleanup_old_files(directory, max_age_hours=1):
    """清理指定目录中的旧文件"""
    try:
        now = datetime.now()
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if now - file_time > timedelta(hours=max_age_hours):
                    os.remove(file_path)
    except Exception as e:
        print(f"清理文件时发生错误: {str(e)}")

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_files():
    if 'template' not in request.files or 'data' not in request.files:
        return jsonify({'error': '请上传模板文件(.txt)和数据文件(.xlsx/.xls)'}), 400
        
    template_file = request.files['template']
    data_file = request.files['data']
    
    if not allowed_file(template_file.filename, 'template'):
        return jsonify({'error': '模板文件格式错误：请上传.txt格式的文本文件，并确保文件使用UTF-8编码'}), 400
    if not allowed_file(data_file.filename, 'data'):
        return jsonify({'error': '数据文件格式错误：请上传.xlsx或.xls格式的Excel文件'}), 400
    
    try:
        # 保存上传的文件
        template_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                   secure_filename(template_file.filename))
        data_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                secure_filename(data_file.filename))
        
        template_file.save(template_path)
        data_file.save(data_path)
        
        # 验证模板和数据
        validator = TemplateValidator()
        is_valid, error_msg = validator.load_template(template_path)
        if not is_valid:
            return jsonify({'error': f'模板文件格式错误：{error_msg}\n请确保模板文件中使用{{字段名}}格式标记变量'}), 400
            
        is_valid, missing_fields, errors = validator.validate_excel(data_path)
        if not is_valid:
            error_messages = []
            for error in errors:
                if '缺少以下字段' in error:
                    error_messages.append(f'数据文件字段缺失：{error}\n请确保Excel表格中的列名与模板中的变量名完全匹配')
                elif '未使用的字段' in error:
                    error_messages.append(f'数据文件包含多余字段：{error}\n这些字段不会影响脚本生成，但建议删除以保持数据整洁')
                elif '存在空值' in error:
                    error_messages.append(f'数据完整性问题：{error}\n请确保所有必填字段都有值')
                else:
                    error_messages.append(f'数据文件错误：{error}')
            return jsonify({
                'error': '\n'.join(error_messages)
            }), 400
        
        # 生成脚本
        generator = ScriptGenerator(validator.template_content)
        output_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'output')
        cleanup_old_files(output_dir)
        
        # 获取总行数
        df = pd.read_excel(data_path)
        total_rows = len(df)
        
        output_file = generator.generate_scripts(data_path, output_dir)
        
        if output_file:
            response = send_file(
                output_file,
                as_attachment=True,
                download_name='generated_scripts.txt',
                mimetype='text/plain'
            )
            
            # 使用TimeTracker更新节省时间
            time_tracker = TimeTracker(current_app)
            saved_time = time_tracker.add_saved_time(total_rows)
            total_saved_time = time_tracker.get_total_saved_time()
            
            # 添加额外的响应头
            response.headers['Content-Type'] = 'text/plain; charset=utf-8'
            response.headers['X-Total-Rows'] = str(total_rows)
            response.headers['X-Saved-Time'] = str(saved_time)
            response.headers['X-Total-Saved-Time'] = str(total_saved_time)
            return response
        else:
            return jsonify({'error': '生成脚本失败，请检查上传的文件是否正确'}), 500
            
    except Exception as e:
        error_msg = str(e)
        if '脚本生成器内部错误' in error_msg:
            return jsonify({'error': '系统内部错误，请联系管理员修复。'}), 500
        elif '数据文件格式错误' in error_msg:
            return jsonify({'error': error_msg}), 400
        elif '生成脚本时发现以下问题' in error_msg:
            return jsonify({'error': '数据处理错误：' + error_msg.replace('生成脚本失败：生成脚本时发现以下问题：', '')}), 400
        else:
            return jsonify({'error': f'处理文件时出错，请检查上传的文件格式是否正确'}), 500

@main.route('/download_template')
def download_template():
    return send_file(
        'static/examples/template_example.txt',
        as_attachment=True,
        download_name='template_example.txt',
        mimetype='text/plain'
    )

@main.route('/download_excel')
def download_excel():
    return send_file(
        'static/examples/data_example.xlsx',
        as_attachment=True,
        download_name='data_example.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )