from __future__ import annotations

import os
import subprocess
import ctypes
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("UPLOAD_ASSISTANT_DATA_DIR", ROOT / "data"))
LOG_DIR = DATA_DIR / "logs"
HOST = os.environ.get("UPLOAD_ASSISTANT_HOST", "127.0.0.1")
PORT = int(os.environ.get("UPLOAD_ASSISTANT_PORT", "8000"))
SERVER_URL = f"http://{HOST}:{PORT}"


def log(message: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(line)
    with (LOG_DIR / "launcher.log").open("a", encoding="utf-8", errors="replace") as file:
        file.write(line + "\n")


def health_ok() -> bool:
    try:
        with urllib.request.urlopen(f"{SERVER_URL}/api/health", timeout=1.5) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def wait_for_health(seconds: int = 20) -> bool:
    deadline = time.time() + seconds
    while time.time() < deadline:
        if health_ok():
            return True
        time.sleep(0.5)
    return False


def python_command() -> list[str]:
    return [sys.executable]


def creationflags() -> int:
    if os.name != "nt":
        return 0
    return subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["UPLOAD_ASSISTANT_HOST"] = HOST
    env["UPLOAD_ASSISTANT_PORT"] = str(PORT)
    env["UPLOAD_ASSISTANT_DATA_DIR"] = str(DATA_DIR)
    env["UPLOAD_ASSISTANT_DB"] = str(DATA_DIR / "app.db")
    return env


def windows_process_running(keyword: str) -> bool:
    if os.name != "nt":
        return False
    try:
        escaped_keyword = keyword.replace("'", "''")
        command = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            "Get-CimInstance Win32_Process | "
            f"Where-Object {{ $_.Name -match '^pythonw?\\.exe$' -and $_.CommandLine -like '*{escaped_keyword}*' }} | "
            "Select-Object -First 1 -ExpandProperty ProcessId",
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=5, creationflags=creationflags())
        return bool(result.stdout.strip())
    except Exception as exc:
        log(f"????????????{exc}")
        return False


def start_backend() -> None:
    if health_ok():
        log("后台已运行，直接复用")
        return
    env = base_env()
    env["UPLOAD_ASSISTANT_OPEN_BROWSER"] = "false"
    stdout = (LOG_DIR / "backend-launch.log").open("a", encoding="utf-8", errors="replace")
    command = [*python_command(), str(ROOT / "backend" / "run_server.py")]
    subprocess.Popen(command, cwd=ROOT, env=env, stdout=stdout, stderr=subprocess.STDOUT, creationflags=creationflags())
    log("后台启动中")
    if not wait_for_health():
        raise RuntimeError("后台启动超时，请查看 data/logs/backend-launch.log")
    log("后台已就绪")


def start_executor() -> None:
    if windows_process_running("windows_executor.py"):
        log("???????????")
        return
    env = base_env()
    work_dir = DATA_DIR / "executor"
    command = [
        *python_command(),
        str(ROOT / "scripts" / "windows_executor.py"),
        "--server",
        SERVER_URL,
        "--work-dir",
        str(work_dir),
        "--publish",
    ]
    stdout = (LOG_DIR / "executor-launch.log").open("a", encoding="utf-8", errors="replace")
    subprocess.Popen(command, cwd=ROOT, env=env, stdout=stdout, stderr=subprocess.STDOUT, creationflags=creationflags())
    log("??????????????")


def open_home_page() -> None:
    try:
        webbrowser.open(SERVER_URL)
        log(f"??????{SERVER_URL}")
    except Exception as exc:
        log(f"????????????? {SERVER_URL}????{exc}")


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log("启动上货助手")
    start_backend()
    start_executor()
    webbrowser.open(SERVER_URL)
    log(f"已打开页面：{SERVER_URL}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        log(f"启动失败：{type(exc).__name__}: {exc}")
        raise
