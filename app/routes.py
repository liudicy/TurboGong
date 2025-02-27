from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import os
from werkzeug.utils import secure_filename
from app.services.template_validator import TemplateValidator
from app.services.script_generator import ScriptGenerator
from datetime import datetime, timedelta
import pandas as pd

# 用于存储总节省时间的变量
total_saved_time = 0

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
        return jsonify({'error': '请选择模板文件和数据文件'}), 400
        
    template_file = request.files['template']
    data_file = request.files['data']
    
    if not allowed_file(template_file.filename, 'template'):
        return jsonify({'error': '模板文件必须是.txt格式'}), 400
    if not allowed_file(data_file.filename, 'data'):
        return jsonify({'error': '数据文件必须是.xlsx或.xls格式'}), 400
    
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
        if not validator.load_template(template_path):
            return jsonify({'error': '模板文件格式错误'}), 400
            
        is_valid, missing_fields = validator.validate_excel(data_path)
        if not is_valid:
            return jsonify({
                'error': f'Excel文件缺少以下字段：{", ".join(missing_fields)}'
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
            # 计算节省时间（每行0.5秒）
            saved_time = total_rows * 0.5
            
            # 更新总节省时间
            global total_saved_time
            total_saved_time += saved_time
            
            # 添加额外的响应头
            response.headers['Content-Type'] = 'text/plain; charset=utf-8'
            response.headers['X-Total-Rows'] = str(total_rows)
            response.headers['X-Saved-Time'] = str(saved_time)
            response.headers['X-Total-Saved-Time'] = str(total_saved_time)
            return response
        else:
            return jsonify({'error': '生成脚本失败'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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