import pandas as pd
import os
import re
from datetime import datetime

class ScriptGenerator:
    def __init__(self, template_content: str):
        self.template_content = template_content

    def generate_scripts(self, excel_path: str, output_dir: str) -> str:
        """根据模板和Excel数据生成脚本文件"""
        try:
            # 读取Excel数据
            df = pd.read_excel(excel_path)
            if df.empty:
                raise ValueError("Excel文件中没有数据")

            all_scripts = []
            errors = []
            
            # 遍历每一行数据生成脚本
            for index, row in df.iterrows():
                try:
                    # 获取当前行的数据字典
                    data_dict = row.to_dict()
                    
                    # 生成脚本内容
                    script_content = self.template_content
                    for field, value in data_dict.items():
                        # 处理数值型数据
                        if pd.isna(value):
                            errors.append(f"第{index + 1}行的{field}字段值为空")
                            value = ''
                        elif isinstance(value, (int, float)):
                            if isinstance(value, int):
                                value = str(value)
                            else:
                                value = str(int(value)) if float(value).is_integer() else str(value)
                        else:
                            value = str(value)
                        
                        script_content = script_content.replace(f"{{{field}}}", value)
                    
                    # 检查是否还有未替换的变量
                    remaining_vars = re.findall(r'\{([^}]+)\}', script_content)
                    if remaining_vars:
                        errors.append(f"第{index + 1}行缺少以下字段的值：{', '.join(remaining_vars)}")
                    
                    all_scripts.append(script_content)
                except Exception as row_error:
                    error_msg = str(row_error)
                    if "KeyError" in error_msg:
                        errors.append(f"处理第{index + 1}行时出错：Excel表格中缺少必要的列，请确保所有模板变量都有对应的数据列")
                    else:
                        errors.append(f"处理第{index + 1}行时出错：{error_msg}")
            
            if errors:
                error_message = "\n".join(errors)
                raise ValueError(f"生成脚本时发现以下问题：\n{error_message}")
            
            # 合并所有脚本，用换行符分隔
            combined_script = "\n\n".join(all_scripts)
            
            # 使用时间戳创建唯一的文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(output_dir, f'generated_scripts_{timestamp}.txt')
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 保存到文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(combined_script)
            
            return output_file
            
        except Exception as e:
            error_msg = str(e)
            if "name 're' is not defined" in error_msg:
                raise ValueError("脚本生成器内部错误：缺少必要的模块。请联系管理员修复此问题。")
            elif "KeyError" in error_msg:
                raise ValueError(f"数据文件格式错误：Excel表格中的列名与模板中的变量名不匹配。请检查Excel文件的列名是否与模板中的{{变量名}}完全一致。")
            else:
                raise ValueError(f"生成脚本失败：{error_msg}")