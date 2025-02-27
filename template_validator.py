import re
from typing import List, Set
import pandas as pd

class TemplateValidator:
    def __init__(self):
        self.template_content = None
        self.template_fields = set()
    
    def load_template(self, template_path: str) -> bool:
        """加载并解析模板文件"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
                # 使用正则表达式提取字段名
                self.template_fields = set(re.findall(r'\{([^}]+)\}', self.template_content))
            return True
        except Exception as e:
            print(f"模板加载失败: {str(e)}")
            return False
    
    def validate_excel(self, excel_path: str) -> tuple[bool, List[str]]:
        """验证Excel文件中是否包含所有模板字段"""
        try:
            df = pd.read_excel(excel_path)
            excel_columns = set(df.columns)
            missing_fields = self.template_fields - excel_columns
            
            if missing_fields:
                return False, list(missing_fields)
            return True, []
            
        except Exception as e:
            print(f"Excel验证失败: {str(e)}")
            return False, [] 