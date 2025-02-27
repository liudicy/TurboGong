import os
import json

class TimeTracker:
    def __init__(self, app):
        self.data_file = os.path.join(app.config['UPLOAD_FOLDER'], 'time_stats.json')
        self.total_saved_time = self._load_saved_time()
    
    def _load_saved_time(self):
        """从文件加载累计节省时间"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    return float(data.get('total_saved_time', 0))
        except (json.JSONDecodeError, ValueError, IOError):
            pass
        return 0.0
    
    def _save_time(self):
        """保存累计节省时间到文件"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump({'total_saved_time': self.total_saved_time}, f)
        except IOError:
            pass
    
    def add_saved_time(self, rows):
        """添加新的节省时间（每行1秒）"""
        saved_time = float(rows)  # 每行1秒
        self.total_saved_time += saved_time
        self._save_time()
        return saved_time
    
    def get_total_saved_time(self):
        """获取累计节省时间"""
        return self.total_saved_time