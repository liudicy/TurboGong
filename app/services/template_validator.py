import re
from typing import List, Set, Tuple
import pandas as pd

class TemplateValidator:
    def __init__(self):
        self.template_content = None
        self.template_fields = set()
    
    def load_template(self, template_path: str) -> Tuple[bool, str]:
        """加载并解析模板文件"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
                if not self.template_content.strip():
                    return False, "模板文件内容为空"
                
                # 使用正则表达式提取字段名
                self.template_fields = set(re.findall(r'\{([^}]+)\}', self.template_content))
                if not self.template_fields:
                    return False, "模板文件中未找到任何变量标记，变量标记应使用{字段名}的格式"
                
                return True, ""
        except UnicodeDecodeError:
            return False, "模板文件编码错误，请确保文件为UTF-8编码"
        except Exception as e:
            return False, f"模板加载失败: {str(e)}"
    
    def validate_excel(self, excel_path: str) -> Tuple[bool, List[str], List[str]]:
        """验证Excel文件中是否包含所有模板字段，并检查数据有效性"""
        try:
            df = pd.read_excel(excel_path)
            if df.empty:
                return False, [], ["Excel文件中没有数据"]
            
            excel_columns = set(df.columns)
            missing_fields = self.template_fields - excel_columns
            extra_fields = excel_columns - self.template_fields
            
            errors = []
            if missing_fields:
                errors.append(f"Excel文件缺少以下字段：{', '.join(missing_fields)}")
            if extra_fields:
                errors.append(f"Excel文件包含以下未使用的字段：{', '.join(extra_fields)}")
                
            # 检查空值
            for field in self.template_fields & excel_columns:
                null_rows = df[df[field].isna()].index.tolist()
                if null_rows:
                    rows_str = ', '.join(str(i + 1) for i in null_rows)
                    errors.append(f"字段 '{field}' 在以下行中存在空值：{rows_str}")
            
            return len(errors) == 0, list(missing_fields), errors
            
        except pd.errors.EmptyDataError:
            return False, [], ["Excel文件为空或格式错误"]
        except Exception as e:
            return False, [], [f"Excel验证失败: {str(e)}"]