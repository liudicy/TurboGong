import pandas as pd
from config_generator import ConfigGenerator

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def read_excel(self):
        """读取Excel文件"""
        try:
            df = pd.read_excel(self.file_path)
            return df
        except Exception as e:
            raise Exception(f"读取Excel文件失败: {str(e)}")
            
    def validate_headers(self, df):
        """验证表头是否符合要求"""
        required_headers = [
            "楼栋", "房间号别名", "PONSN", "OLT IP", 
            "槽位", "端口", "ONU编号",
            "内层VLAN", "管理外层VLAN", "管理内层VLAN", "管理UserVLAN",
            "有线1外层VLAN", "有线1内层VLAN", "有线1UserVLAN",
            "无线2G外层VLAN", "无线2G内层VLAN", "无线2GUserVLAN",
            "无线5G外层VLAN", "无线5G内层VLAN", "无线5GUserVLAN"
        ]
        
        # 检查表头是否存在空格，如果存在则去除
        df.columns = df.columns.str.strip()
        
        missing_headers = [header for header in required_headers if header not in df.columns]
        if missing_headers:
            raise Exception(f"缺少必要的表头: {', '.join(missing_headers)}")
            
    def process_data(self, df):
        """处理Excel数据"""
        try:
            # 验证表头
            self.validate_headers(df)
            
            # 按楼栋、槽位、端口、ONU编号排序
            df = df.sort_values(['楼栋', '槽位', '端口', 'ONU编号'])
            
            # 创建配置生成器
            generator = ConfigGenerator()
            
            # 生成所有配置
            all_configs = []
            for _, row in df.iterrows():
                config = generator.generate_config(row)
                all_configs.append(config)
            
            return '\n'.join(all_configs)
            
        except Exception as e:
            raise Exception(f"处理数据失败: {str(e)}") 