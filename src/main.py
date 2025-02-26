import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QLabel, QFileDialog, QWidget, QMessageBox)
from PyQt6.QtCore import Qt
from excel_processor import ExcelProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OLT配置脚本生成工具 By 刘迪")
        self.setFixedSize(500, 200)
        
        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建选择文件按钮
        self.select_button = QPushButton("选择Excel文件")
        self.select_button.clicked.connect(self.select_file)
        self.select_button.setFixedWidth(200)
        
        # 文件路径标签
        self.file_label = QLabel("未选择文件")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setWordWrap(True)
        
        # 处理按钮
        self.process_button = QPushButton("开始处理")
        self.process_button.clicked.connect(self.process_excel)
        self.process_button.setFixedWidth(200)
        
        # 添加部件到布局
        layout.addWidget(self.select_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)
        layout.addWidget(self.process_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.selected_file = None
        
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择Excel文件",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            self.selected_file = file_path
            # 获取文件名，而不是完整路径
            file_name = file_path.split('/')[-1]
            self.file_label.setText(f"已选择: {file_name}")
            
    def process_excel(self):
        if not self.selected_file:
            QMessageBox.warning(self, "警告", "请先选择Excel文件！")
            return
            
        try:
            processor = ExcelProcessor(self.selected_file)
            df = processor.read_excel()
            result = processor.process_data(df)
            
            # 选择保存位置
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存配置文件",
                "config.txt",
                "Text Files (*.txt)"
            )
            
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                QMessageBox.information(self, "成功", "配置文件生成成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 




