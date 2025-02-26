# OLT配置脚本生成工具

一个用于批量生成 OLT 设备配置脚本的图形界面工具。通过读取标准格式的 Excel 文件，自动生成设备配置脚本。

## 功能介绍

- 通过图形界面选择 Excel 文件
- 自动验证 Excel 文件格式和必要字段
- 按楼栋、槽位、端口、ONU编号排序生成配置
- 支持批量生成配置脚本
- 可选择配置文件保存位置
- 完整的错误提示和处理机制

### Excel 文件要求
必须包含以下字段（表头）：
- 楼栋
- 房间号别名
- PONSN
- OLT IP
- 槽位
- 端口
- ONU编号
- 内层VLAN
- 管理外层VLAN
- 管理内层VLAN
- 管理UserVLAN
- 有线1外层VLAN
- 有线1内层VLAN
- 有线1UserVLAN
- 无线2G外层VLAN
- 无线2G内层VLAN
- 无线2GUserVLAN
- 无线5G外层VLAN
- 无线5G内层VLAN
- 无线5GUserVLAN

## 项目结构 
TurboGong/
├── requirements.txt # 项目依赖
├── build.py # 打包脚本
├── setup.py # 包安装配置
├── README.md # 项目说明文档
├── src/ # 源代码目录
│ ├── init.py
│ ├── main.py # 主程序入口
│ ├── excel_processor.py # Excel处理模块
│ └── config_generator.py # 配置生成模块
├── dist/ # 打包输出目录
└── build/ # 打包临时文件

## 开发环境配置

1. 克隆项目并创建虚拟环境：


## 开发环境配置

1. 克隆项目并创建虚拟环境：

```bash
git clone [项目地址]
cd TurboGong
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 打包说明

### Windows 环境打包
```bash
# 在项目根目录执行
python build.py
```
打包后的可执行文件将在 `dist` 目录下生成。

### 其他环境打包注意事项
- 建议在目标运行平台上进行打包
- macOS/Linux 上打包 Windows 版本需要使用虚拟机或 Wine

## 后续开发指南

### 添加新功能
1. 修改配置模板：
   - 编辑 `src/config_generator.py` 中的 `config_template`

2. 更新 Excel 处理：
   - 在 `src/excel_processor.py` 中修改 `validate_headers` 和 `process_data` 方法

3. 更新界面：
   - 在 `src/main.py` 中修改 `MainWindow` 类

### 注意事项
- 保持代码结构清晰
- 添加适当的错误处理
- 更新文档和依赖说明

## 依赖说明

- Python >= 3.9
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- PyQt6 >= 6.4.0
- pyinstaller >= 6.0.0（仅打包需要）

## 作者

刘迪

## 许可证

[添加许可证信息] 