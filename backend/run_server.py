from __future__ import annotations

import os
import socket
import sys
import traceback
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path
from threading import Timer

import uvicorn


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def runtime_dir() -> Path:
    default_dir = ROOT_DIR / "data"
    return Path(os.environ.get("UPLOAD_ASSISTANT_DATA_DIR", default_dir))


def log_startup_error(message: str) -> None:
    log_dir = runtime_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    with (log_dir / "app.log").open("a", encoding="utf-8") as file:
        file.write(message.rstrip() + "\n")


def port_accepts_connections(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex((host, port)) == 0


def local_app_is_running(host: str, port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://{host}:{port}/api/health", timeout=0.75) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def first_available_port(host: str, preferred_port: int) -> int:
    for port in range(preferred_port, preferred_port + 20):
        if not port_accepts_connections(host, port):
            return port
    raise RuntimeError(f"没有可用端口：{preferred_port}-{preferred_port + 19}")


def main() -> None:
    host = os.environ.get("UPLOAD_ASSISTANT_HOST", "127.0.0.1")
    preferred_port = int(os.environ.get("UPLOAD_ASSISTANT_PORT", "8000"))
    open_browser = os.environ.get("UPLOAD_ASSISTANT_OPEN_BROWSER", "true").lower() in {"1", "true", "yes", "on"}
    if local_app_is_running(host, preferred_port):
        if open_browser:
            webbrowser.open(os.environ.get("UPLOAD_ASSISTANT_BROWSER_URL") or f"http://{host}:{preferred_port}")
        return
    port = first_available_port(host, preferred_port)
    browser_url = os.environ.get("UPLOAD_ASSISTANT_BROWSER_URL") or f"http://{host}:{port}"
    try:
        if open_browser:
            Timer(1.2, lambda: webbrowser.open(browser_url)).start()
        uvicorn.run("backend.app.main:app", host=host, port=port, reload=False, access_log=False)
    except Exception:
        log_startup_error(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
