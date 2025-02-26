import PyInstaller.__main__
import sys
import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'src/main.py',  # 主程序文件
    '--name=OLT配置生成工具',  # 生成的exe文件名
    '--windowed',  # 不显示控制台窗口
    '--onefile',  # 打包成单个文件
    '--clean',  # 清理临时文件
    f'--distpath={os.path.join(current_dir, "dist")}',  # 输出目录
    f'--workpath={os.path.join(current_dir, "build")}',  # 工作目录
    f'--specpath={os.path.join(current_dir, "build")}',  # spec文件目录
]) 