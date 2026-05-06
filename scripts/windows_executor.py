"""Windows upload executor.

Polls the server for queued upload tasks, runs the local Dianxiaomi RPA on this
Windows machine, and reports the result back to the server.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_RPA_DIR = Path(r"C:\Users\zyf\.accio\accounts\1753260534\agents\MID-27260534U1775454-06F6F0-2183-EB2CBD\project")


def request_json(method: str, url: str, payload: dict | None = None, timeout: int = 60) -> dict:
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw else {}


def download_file(url: str, target: Path, timeout: int = 300) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        target.write_bytes(resp.read())
    return target


def normalize_server_url(value: str) -> str:
    return value.strip().rstrip("/")


def absolute_url(server_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return normalize_server_url(server_url) + "/" + path.lstrip("/")


def count_success(stdout_text: str) -> tuple[int, int, str]:
    if "完成：成功" in stdout_text or "完成:成功" in stdout_text:
        import re

        match = re.search(r"完成[：:]成功\s*(\d+)\s*个[，,]\s*失败/跳过\s*(\d+)\s*个", stdout_text)
        if match:
            success = int(match.group(1))
            failed = int(match.group(2))
            return success, failed, "rpa_success" if success > 0 and failed == 0 else "rpa_failed"
    failure_markers = ["导入提交失败", "已停止后续上图", "未获取到待检测的产品货号", "超时仍未就绪", "完成：成功 0 个"]
    if any(marker in stdout_text for marker in failure_markers):
        return 0, 1, "rpa_failed"
    return 0, 0, "rpa_failed"


def run_rpa(rpa_dir: Path, xlsx_path: Path, manifest: dict, no_publish: bool) -> tuple[str, int, int, str]:
    product_ids = []
    for item in manifest.get("items", []) if isinstance(manifest.get("items"), list) else []:
        skc = str(item.get("skc", "")).strip()
        if skc and skc not in product_ids:
            product_ids.append(skc)
    if not product_ids:
        raise RuntimeError("manifest 中没有可执行 SKC")

    command = [sys.executable, "rpa_upload.py", *product_ids, "--import", str(xlsx_path)]
    if no_publish:
        command.append("--no-publish")

    settings = manifest.get("settings", {}) if isinstance(manifest.get("settings"), dict) else {}
    upload = settings.get("flow", {}) if isinstance(settings.get("flow"), dict) else {}
    templates = settings.get("temu", {}) if isinstance(settings.get("temu"), dict) else {}

    image_source = str(upload.get("image_source", "")).strip()
    if image_source:
        command += ["--image-source", image_source]

    template_arg_map = {
        "shop_account": "--shop-account",
        "site": "--site",
        "product_template": "--product-template",
        "size_template": "--size-template",
        "warehouse_template": "--warehouse-template",
        "logistics_template": "--logistics-template",
    }
    for key, arg in template_arg_map.items():
        value = str(templates.get(key, "")).strip()
        if value:
            command += [arg, value]

    print("执行命令：", " ".join(command))
    completed = subprocess.run(command, cwd=rpa_dir, capture_output=True, text=True, timeout=60 * 60, check=False)
    stdout_text = (completed.stdout or "") + "\n" + (completed.stderr or "")
    success_count, failed_count, status = count_success(stdout_text)
    if completed.returncode != 0:
        status = "rpa_failed"
    return stdout_text, success_count, failed_count, status


def process_once(server_url: str, executor_id: str, rpa_dir: Path, work_dir: Path, no_publish: bool) -> bool:
    claim = request_json("POST", absolute_url(server_url, "/api/executor/tasks/claim"), {"executor_id": executor_id, "version": "0.1.0"})
    if not claim.get("task"):
        print("暂无待上货任务")
        return False

    task = claim["task"]
    task_id = int(task["id"])
    print(f"领取任务 #{task_id}: {task.get('name', '')}")
    request_json("POST", absolute_url(server_url, f"/api/executor/tasks/{task_id}/heartbeat"), {"executor_id": executor_id})

    export_url = absolute_url(server_url, claim.get("export_download_url", ""))
    filename = Path(urllib.parse.urlparse(export_url).path).name or f"upload_task_{task_id}.xlsx"
    xlsx_path = download_file(export_url, work_dir / "downloads" / filename)
    print(f"下载导入表：{xlsx_path}")

    try:
        stdout_text, success_count, failed_count, status = run_rpa(rpa_dir, xlsx_path, claim.get("manifest", {}), no_publish=no_publish)
        run_log = f"Windows executor finished task {task_id}: {status}"
    except Exception as exc:
        stdout_text = repr(exc)
        success_count = 0
        failed_count = 1
        status = "rpa_failed"
        run_log = f"Windows executor exception: {exc}"

    request_json(
        "POST",
        absolute_url(server_url, f"/api/executor/tasks/{task_id}/report"),
        {
            "executor_id": executor_id,
            "status": status,
            "success_count": success_count,
            "failed_count": failed_count,
            "run_log": run_log,
            "stdout": stdout_text[-50000:],
        },
        timeout=120,
    )
    print(f"已回传任务 #{task_id}: {status}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll server upload tasks and run local Windows RPA.")
    parser.add_argument("--server", default="http://124.156.175.191", help="Server URL")
    parser.add_argument("--executor-id", default=f"windows-{socket.gethostname()}", help="Executor ID")
    parser.add_argument("--rpa-dir", default=str(DEFAULT_RPA_DIR), help="Local RPA project directory")
    parser.add_argument("--work-dir", default=str(Path(__file__).resolve().parents[1] / "data" / "executor"), help="Local executor work directory")
    parser.add_argument("--poll", type=int, default=5, help="Poll interval seconds")
    parser.add_argument("--once", action="store_true", help="Run one poll cycle and exit")
    parser.add_argument("--publish", action="store_true", help="Actually publish. Default keeps --no-publish for safety.")
    args = parser.parse_args()

    server_url = normalize_server_url(args.server)
    rpa_dir = Path(args.rpa_dir)
    work_dir = Path(args.work_dir)
    if not (rpa_dir / "rpa_upload.py").exists():
        raise SystemExit(f"RPA script not found: {rpa_dir / 'rpa_upload.py'}")

    while True:
        try:
            process_once(server_url, args.executor_id, rpa_dir, work_dir, no_publish=not args.publish)
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"连接服务器失败：{exc}")
        if args.once:
            break
        time.sleep(max(args.poll, 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
