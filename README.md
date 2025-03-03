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

## 安装部署

### 开发环境

1. 克隆项目：
```bash
git clone https://github.com/yourusername/TurboGong.git
cd TurboGong
```

2. 创建并激活虚拟环境：
```bash
# 创建虚拟环境
python3 -m venv venv

# Linux/macOS 激活虚拟环境
. venv/bin/activate
# 或者
source ./venv/bin/activate

# Windows 激活虚拟环境
.\venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行开发服务器：
```bash
python run.py
```

5. 访问服务：
打开浏览器访问 http://localhost:5000

### 生产环境部署

1. 安装系统依赖：
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-venv nginx supervisor

# CentOS/RHEL
sudo yum install python3-venv nginx supervisor
```

2. 克隆项目并设置虚拟环境：
```bash
# 克隆到指定目录
cd /var/www
git clone https://github.com/yourusername/TurboGong.git
cd TurboGong

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn
```

3. 配置Supervisor：
创建配置文件 `/etc/supervisor/conf.d/turbogong.conf`：
```ini
[program:turbogong]
directory=/var/www/TurboGong
command=/var/www/TurboGong/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 run:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/turbogong/err.log
stdout_logfile=/var/log/turbogong/out.log
```

4. 配置Nginx：
创建配置文件 `/etc/nginx/sites-available/turbogong`：
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. 启动服务：
```bash
# 创建日志目录
sudo mkdir -p /var/log/turbogong
sudo chown www-data:www-data /var/log/turbogong

# 启用Nginx配置
sudo ln -s /etc/nginx/sites-available/turbogong /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 启动Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start turbogong
```

## 使用说明

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
- Excel表格的列名必须与模板中的字段名完全匹配
- 可下载示例表格参考格式

### 使用步骤
1. 访问Web界面
2. 上传模板文件和Excel数据文件
3. 点击"生成脚本"按钮
4. 自动下载生成的脚本文件

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

## 注意事项

- 确保上传的Excel文件字段名与模板中的变量名完全匹配
- 生成的脚本文件为纯文本格式
- 临时文件会定期自动清理
- 建议使用现代浏览器访问

## 许可证

MIT