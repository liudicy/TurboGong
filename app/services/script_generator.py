import pandas as pd
import os
from datetime import datetime

class ScriptGenerator:
    def __init__(self, template_content: str):
        self.template_content = template_content

    def generate_scripts(self, excel_path: str, output_dir: str) -> str:
        """根据模板和Excel数据生成脚本文件"""
        try:
            # 读取Excel数据
            df = pd.read_excel(excel_path)
            all_scripts = []
            
            # 遍历每一行数据生成脚本
            for index, row in df.iterrows():
                # 获取当前行的数据字典
                data_dict = row.to_dict()
                
                # 生成脚本内容
                script_content = self.template_content
                for field, value in data_dict.items():
                    # 处理数值型数据
                    if pd.isna(value):
                        value = ''
                    elif isinstance(value, (int, float)):
                        value = str(int(value)) if value.is_integer() else str(value)
                    else:
                        value = str(value)
                    
                    script_content = script_content.replace(f"{{{field}}}", value)
                
                all_scripts.append(script_content)
            
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
            print(f"生成脚本时发生错误: {str(e)}")
            return None 