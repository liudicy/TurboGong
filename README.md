# 脚本生成工具

一个基于Web的配置脚本生成工具。支持自定义模板，通过上传Excel文件批量生成配置脚本。

## 功能特点

- 基于Web界面，支持各种终端访问
- 支持自定义文本模板
- 支持Excel数据导入
- 自动验证模板字段与Excel数据的匹配性
- 批量生成脚本文件
- 美观的用户界面
- 完整的错误提示

## 使用说明

1. 准备模板文件 (.txt格式)
   - 使用{字段名}标注需要替换的变量
   - 示例：`设备名称：{device_name}，IP地址：{ip_address}`
   - 可下载示例模板参考

2. 准备Excel数据文件 (.xlsx/.xls格式)
   - Excel表格的列名必须与模板中的字段名完全匹配
   - 可下载示例表格参考

3. 使用步骤
   - 访问Web界面
   - 上传模板文件和Excel数据文件
   - 点击"生成脚本"按钮
   - 自动下载生成的脚本文件

## 安装部署

1. 克隆项目：
```bash
git clone [项目地址]
cd TurboGong
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行服务：
```bash
python run.py
```

5. 访问服务：
打开浏览器访问 http://localhost:5000

## 项目结构

```
TurboGong/
├── README.md              # 项目说明文档
├── requirements.txt       # 项目依赖
├── run.py                # 程序入口
├── app/                  # 应用目录
│   ├── __init__.py      # 应用初始化
│   ├── routes.py        # 路由处理
│   ├── services/        # 业务逻辑目录
│   │   ├── template_validator.py  # 模板验证
│   │   └── script_generator.py    # 脚本生成
│   ├── static/          # 静态资源
│   └── templates/       # HTML模板
└── uploads/             # 上传文件目录
```

## 开发说明

- 使用 Flask 框架开发
- 前端采用原生 JavaScript
- 设计风格参考 Apple 官网
- 模块化设计，便于扩展

## 注意事项

- 确保上传的Excel文件字段名与模板中的变量名完全匹配
- 生成的脚本文件为纯文本格式
- 临时文件会定期自动清理
- 建议使用现代浏览器访问

## 许可证

MIT

## 功能介绍

- 支持自定义文本模板
- 通过图形界面选择模板和 Excel 文件
- 自动验证 Excel 文件与模板字段的匹配性
- 按楼栋、槽位、端口、ONU编号排序生成配置
- 支持批量生成配置脚本
- 可选择配置文件保存位置
- 完整的错误提示和处理机制

### 模板文件要求
- 文件格式：.txt
- 使用 {字段名} 标记需要替换的变量
- 示例：
```configure terminal 
interface gpon-olt_1/{槽位}/{端口}
  onu {ONU编号} type ZTEG-F660 sn {PONSN}  
!
```

### Excel 文件要求
Excel 文件的列名必须与模板中使用的字段名完全匹配。例如，如果模板中使用了 {槽位}，Excel 中就必须有一列名为"槽位"。

常用字段示例：
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