import pandas as pd
from typing import Dict, List
import os

class ConfigGenerator:
    def __init__(self, template_content: str):
        self.template_content = template_content

    def generate_scripts(self, excel_path: str, output_dir: str) -> List[str]:
        """根据模板和Excel数据生成脚本文件"""
        try:
            # 读取Excel数据
            df = pd.read_excel(excel_path)
            generated_files = []
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
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
                
                # 生成文件名（使用行号或特定字段）
                filename = f"script_{index + 1}.txt"
                file_path = os.path.join(output_dir, filename)
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                
                generated_files.append(file_path)
            
            return generated_files
            
        except Exception as e:
            print(f"生成脚本时发生错误: {str(e)}")
            return []

    def generate_config(self, row_data):
        """根据每行数据生成配置"""
        try:
            return self.template_content.format(**row_data)
        except KeyError as e:
            raise Exception(f"数据缺少必要字段: {str(e)}")

    def save_config(self, config, output_path):
        """保存生成的配置到文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(config)
        except Exception as e:
            raise Exception(f"保存配置文件失败: {str(e)}") 