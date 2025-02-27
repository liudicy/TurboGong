import sys
import os
import platform

def check_environment():
    """检查运行环境"""
    try:
        import tkinter
    except ImportError:
        print("错误: 缺少 tkinter 模块")
        print("\n请按照以下步骤安装：")
        
        system = platform.system()
        if system == "Darwin":  # macOS
            print("在 macOS 上运行以下命令：")
            print("brew install python-tk@3.13")
        elif system == "Linux":
            print("在 Linux 上运行以下命令：")
            print("sudo apt-get install python3-tk  # Ubuntu/Debian")
            print("或")
            print("sudo dnf install python3-tkinter  # Fedora")
        elif system == "Windows":
            print("在 Windows 上：")
            print("1. 重新安装 Python，确保在安装时选中 'tcl/tk and IDLE'")
            print("2. 或使用 pip 安装：pip install tk")
        
        sys.exit(1)

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.script_generator_ui import ScriptGeneratorUI

def main():
    """主程序入口"""
    try:
        # 检查环境
        check_environment()
        
        # 导入必要模块
        from src.script_generator_ui import ScriptGeneratorUI
        
        # 运行程序
        app = ScriptGeneratorUI()
        app.run()
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 




