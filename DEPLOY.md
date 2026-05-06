# 服务器部署说明

## 适用范围

本说明用于把 `upload-assistant` 部署到服务器运行后台与前端页面。

注意：真实店小秘 RPA 依赖浏览器、店小秘登录态、COS 密钥和 RPA 脚本路径。迁移到服务器后，需要在服务器上重新配置这些运行项；不能直接复用本机 Windows 路径。

## 服务器要求

- Python 3.10+
- Git
- 可访问 GitHub
- 可开放一个 Web 端口，例如 `8000`
- 如需真实 RPA：安装 Playwright 浏览器依赖，并重新登录店小秘保存 cookies

## 拉取源码

```bash
cd /opt
git clone https://github.com/himalt/my.git upload-assistant
cd /opt/upload-assistant
```

## 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 数据目录

默认数据目录是项目内 `data/`，首次启动会自动创建数据库。

也可以指定独立目录：

```bash
export UPLOAD_ASSISTANT_DATA_DIR=/data/upload-assistant
```

## 启动后台

```bash
source .venv/bin/activate
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

访问：

```text
http://服务器IP:8000
```

## systemd 守护进程

创建 `/etc/systemd/system/upload-assistant.service`：

```ini
[Unit]
Description=Upload Assistant
After=network.target

[Service]
WorkingDirectory=/opt/upload-assistant
Environment=UPLOAD_ASSISTANT_DATA_DIR=/data/upload-assistant
ExecStart=/opt/upload-assistant/.venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启动：

```bash
sudo mkdir -p /data/upload-assistant
sudo systemctl daemon-reload
sudo systemctl enable --now upload-assistant
sudo systemctl status upload-assistant
```

## 真实 RPA 迁移检查

后台启动后，在页面里重新配置：

1. API 设置：OpenAI/DeepSeek、图片 API、COS 等密钥
2. 1688 Cookie 或万邦 API
3. 店铺与模板：店铺、站点、产品模板、尺码模板、仓库模板、物流模板
4. RPA 路径：服务器上的 `rpa/rpa_upload.py` 或实际 RPA 脚本路径
5. 店小秘登录态：服务器浏览器环境重新登录并保存 cookies

## 更新代码

```bash
cd /opt/upload-assistant
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart upload-assistant
```
