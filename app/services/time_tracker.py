import os
import json
import logging

class TimeTracker:
    def __init__(self, app):
        self.data_file = os.path.join(app.config['UPLOAD_FOLDER'], 'time_stats.json')
        self.total_saved_time = self._load_saved_time()
    
    def _check_file_permissions(self):
        """检查文件权限"""
        dir_path = os.path.dirname(self.data_file)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError as e:
                logging.error(f'创建目录失败: {e}')
                return False
        
        # 检查文件是否存在，如果不存在则创建
        if not os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'w') as f:
                    json.dump({'total_saved_time': 0.0}, f)
            except IOError as e:
                logging.error(f'创建文件失败: {e}')
                return False
        
        # 检查文件读写权限
        return os.access(self.data_file, os.R_OK | os.W_OK)
    
    def _load_saved_time(self):
        """从文件加载累计节省时间"""
        if not self._check_file_permissions():
            logging.error('文件权限检查失败，无法加载数据')
            return 0.0
            
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return float(data.get('total_saved_time', 0))
        except json.JSONDecodeError as e:
            logging.error(f'JSON解析错误: {e}')
        except ValueError as e:
            logging.error(f'数值转换错误: {e}')
        except IOError as e:
            logging.error(f'文件读取错误: {e}')
        except Exception as e:
            logging.error(f'加载数据时发生未知错误: {e}')
        return 0.0
    
    def _save_time(self):
        """保存累计节省时间到文件"""
        if not self._check_file_permissions():
            logging.error('文件权限检查失败，无法保存数据')
            return False
            
        try:
            with open(self.data_file, 'w') as f:
                json.dump({'total_saved_time': self.total_saved_time}, f)
            return True
        except IOError as e:
            logging.error(f'保存数据时发生错误: {e}')
        except Exception as e:
            logging.error(f'保存数据时发生未知错误: {e}')
        return False
    
    def add_saved_time(self, rows):
        """添加新的节省时间（每行0.5秒）"""
        try:
            saved_time = float(rows) * 0.5  # 每行0.5秒
            self.total_saved_time += saved_time
            if not self._save_time():
                logging.warning('保存累计时间失败')
            return saved_time
        except ValueError as e:
            logging.error(f'转换行数时发生错误: {e}')
            return 0.0
    
    def get_total_saved_time(self):
        """获取累计节省时间"""
        return self.total_saved_time