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