"""Windows upload executor.

Polls the server for queued upload tasks, runs the local Dianxiaomi RPA on this
Windows machine, and reports the result back to the server.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_RPA_DIR = Path(r"C:\Users\zyf\.accio\accounts\1753260534\agents\MID-27260534U1775454-06F6F0-2183-EB2CBD\project")


class TeeOutput:
    def __init__(self, *targets):
        self.targets = targets

    def write(self, text: str) -> int:
        for target in self.targets:
            target.write(text)
            target.flush()
        return len(text)

    def flush(self) -> None:
        for target in self.targets:
            target.flush()


def setup_executor_logging(work_dir: Path):
    log_dir = executable_dir() / "data" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = (log_dir / "executor-launch.log").open("a", encoding="utf-8", errors="replace")
    return contextlib.ExitStack(), log_file, log_dir / "executor-launch.log"


def executable_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def resolve_rpa_dir(value: str) -> Path:
    candidates = [Path(value)] if value else []
    base_dir = executable_dir()
    candidates.extend(
        [
            base_dir / "rpa",
            base_dir / "店小秘RPA",
            base_dir / "dxm-rpa",
            base_dir,
            DEFAULT_RPA_DIR,
        ]
    )
    for candidate in candidates:
        try:
            resolved = candidate.expanduser().resolve()
        except OSError:
            resolved = candidate.expanduser()
        if (resolved / "rpa_upload.py").exists():
            return resolved
    checked = "\n".join(str(candidate) for candidate in candidates)
    raise SystemExit(f"未找到店小秘 RPA 脚本 rpa_upload.py。请把 RPA 项目放到客户端目录的 rpa 文件夹，或用 --rpa-dir 指定。已检查：\n{checked}")


def resolve_rpa_python(rpa_dir: Path) -> str:
    candidates = [
        rpa_dir / ".venv" / "Scripts" / "python.exe",
        rpa_dir / "venv" / "Scripts" / "python.exe",
        rpa_dir / "env" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    python_exe = shutil.which("python") or shutil.which("py")
    if python_exe:
        return python_exe
    raise SystemExit("未找到可运行 RPA 的 Python。请在这台电脑安装 Python，或在 RPA 项目里准备 .venv\\Scripts\\python.exe。")


def resolve_rpa_entry(rpa_dir: Path) -> list[str]:
    exe_path = rpa_dir / "rpa_upload.exe"
    if exe_path.exists():
        return [str(exe_path)]
    return [resolve_rpa_python(rpa_dir), "rpa_upload.py"]


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


def executor_runtime_dir(work_dir: Path) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    return work_dir


def write_executor_status(work_dir: Path, executor_id: str, status: str, message: str = "", task_id: int = 0) -> None:
    payload = {
        "executor_id": executor_id,
        "status": status,
        "message": message,
        "task_id": task_id,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    status_path = executor_runtime_dir(work_dir) / "status.json"
    status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def pending_result_dir(work_dir: Path) -> Path:
    path = executor_runtime_dir(work_dir) / "pending_results"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_pending_result(work_dir: Path, task_id: int, payload: dict) -> Path:
    target = pending_result_dir(work_dir) / f"task_{task_id}.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def flush_pending_results(server_url: str, work_dir: Path) -> None:
    for path in sorted(pending_result_dir(work_dir).glob("task_*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            task_id = int(payload.get("task_id") or 0)
            report = payload.get("report") if isinstance(payload.get("report"), dict) else {}
            if task_id <= 0 or not report:
                path.unlink(missing_ok=True)
                continue
            request_json("POST", absolute_url(server_url, f"/api/executor/tasks/{task_id}/report"), report, timeout=120)
            path.unlink(missing_ok=True)
            print(f"已补传本地结果: task #{task_id}")
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"本地结果补传失败，稍后重试: {path.name}: {exc}")
            return
        except Exception as exc:
            print(f"本地结果文件异常，保留待人工检查: {path}: {type(exc).__name__}: {exc}")


def download_file(url: str, target: Path, timeout: int = 300) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        target.write_bytes(resp.read())
    return target


def safe_xlsx_filename(claim: dict, task_id: int, export_url: str) -> str:
    candidates = [
        str(claim.get("export_filename") or ""),
        Path(urllib.parse.urlparse(export_url).path).name,
        f"upload_task_{task_id}.xlsx",
    ]
    for candidate in candidates:
        filename = Path(candidate).name.strip()
        if not filename:
            continue
        if filename.lower().endswith(".xlsx"):
            return filename
        if filename in {"export", "download"} or "." not in filename:
            return f"upload_task_{task_id}.xlsx"
    return f"upload_task_{task_id}.xlsx"


def normalize_server_url(value: str) -> str:
    return value.strip().rstrip("/")


def absolute_url(server_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return normalize_server_url(server_url) + "/" + path.lstrip("/")


def count_result(stdout_text: str) -> tuple[int, int, str]:
    patterns = [
        r"完成[:：]\s*成功\s*(\d+)\s*个[，,]\s*失败/跳过\s*(\d+)\s*个",
        r"完成[:：]\s*成功\s*(\d+)\s*个[，,]\s*失败\s*(\d+)\s*个",
    ]
    for pattern in patterns:
        match = re.search(pattern, stdout_text)
        if match:
            success = int(match.group(1))
            failed = int(match.group(2))
            return success, failed, "rpa_success" if success > 0 and failed == 0 else "rpa_failed"
    failure_markers = [
        "导入提交失败",
        "已停止后续上图",
        "未获取到待检测的产品货号",
        "超时仍未就绪",
        "完成：成功 0 个",
        "完成: 成功 0 个",
    ]
    if any(marker in stdout_text for marker in failure_markers):
        return 0, 1, "rpa_failed"
    return 0, 0, "rpa_failed"


def summarize_failure(stdout_text: str, run_log: str = "") -> tuple[str, str, str]:
    combined = "\n".join(part for part in [run_log, stdout_text] if part).strip()
    if not combined:
        return "executor", "执行器未返回失败详情", ""
    stage_patterns = [
        ("import", ["导入", "import"]),
        ("ready-check", ["就绪", "搜索", "ready"]),
        ("open-edit", ["编辑", "open-edit"]),
        ("apply-template", ["模板", "template"]),
        ("upload-color-images", ["上传", "图片", "file chooser", "image"]),
        ("prune-empty-colors", ["剪枝", "无图", "prune"]),
        ("fill-size-chart", ["尺码", "size"]),
        ("select-warehouse", ["仓库", "warehouse"]),
        ("fill-batch-inventory", ["库存", "inventory"]),
        ("save", ["保存", "错误", "save"]),
    ]
    lower_text = combined.lower()
    stage = "rpa"
    for candidate, keywords in stage_patterns:
        if any(keyword.lower() in lower_text for keyword in keywords):
            stage = candidate
            break
    lines = [line.strip() for line in combined.splitlines() if line.strip()]
    reason = ""
    for line in reversed(lines):
        if any(keyword in line for keyword in ["失败", "错误", "Exception", "Traceback", "Timeout", "ERROR", "fail", "Failed"]):
            reason = line
            break
    if not reason and lines:
        reason = lines[-1]
    evidence = ""
    for match in re.finditer(r"[A-Za-z]:[^\r\n<>|?*]+?\.(?:png|jpg|jpeg|html|log|txt)", combined, re.I):
        evidence = match.group(0).strip().strip("'\")")
    return stage, reason[:500], evidence


def task_skc_values(manifest: dict) -> list[str]:
    product_ids: list[str] = []
    items = manifest.get("items", [])
    if not isinstance(items, list):
        return product_ids
    for item in items:
        if not isinstance(item, dict):
            continue
        skc = str(item.get("skc", "")).strip()
        if skc and skc not in product_ids:
            product_ids.append(skc)
    return product_ids


def build_rpa_command(rpa_dir: Path, xlsx_path: Path, manifest: dict, no_publish: bool) -> list[str]:
    product_ids = task_skc_values(manifest)
    if not product_ids:
        raise RuntimeError("manifest 中没有可执行 SKC")

    command = [*resolve_rpa_entry(rpa_dir), *product_ids, "--import", str(xlsx_path.resolve())]
    if no_publish:
        command.append("--no-publish")

    settings = manifest.get("settings", {}) if isinstance(manifest.get("settings"), dict) else {}
    upload = settings.get("flow", {}) if isinstance(settings.get("flow"), dict) else {}
    templates = settings.get("temu", {}) if isinstance(settings.get("temu"), dict) else {}

    if str(upload.get("save_screenshots", "false")).lower() == "true":
        command.append("--debug-shots")

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
    return command


def sync_rpa_images_to_default_dir(rpa_dir: Path, manifest: dict) -> None:
    rpa_images = manifest.get("rpa_images", {}) if isinstance(manifest.get("rpa_images"), dict) else {}
    source_root = Path(str(rpa_images.get("root", "")).strip())
    if not source_root.exists() or not source_root.is_dir():
        return
    target_root = rpa_dir / "data" / "sku_images"
    if target_root.resolve() == source_root.resolve():
        return
    target_root.mkdir(parents=True, exist_ok=True)
    for source_item in source_root.iterdir():
        target_item = target_root / source_item.name
        if target_item.exists():
            if target_item.is_dir():
                shutil.rmtree(target_item)
            else:
                target_item.unlink()
        if source_item.is_dir():
            shutil.copytree(source_item, target_item)
        else:
            shutil.copy2(source_item, target_item)


def run_rpa(rpa_dir: Path, xlsx_path: Path, manifest: dict, no_publish: bool) -> tuple[str, int, int, str]:
    sync_rpa_images_to_default_dir(rpa_dir, manifest)
    command = build_rpa_command(rpa_dir, xlsx_path, manifest, no_publish)
    print("执行命令:", " ".join(command))
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    process = subprocess.Popen(command, cwd=rpa_dir, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    output_lines: list[str] = []
    deadline = time.time() + 60 * 60
    assert process.stdout is not None
    while True:
        if time.time() > deadline:
            process.kill()
            raise TimeoutError("RPA 执行超过 60 分钟")
        line = process.stdout.readline()
        if line:
            print(line, end="")
            output_lines.append(line)
            continue
        if process.poll() is not None:
            remainder = process.stdout.read()
            if remainder:
                print(remainder, end="")
                output_lines.append(remainder)
            break
        time.sleep(0.2)
    return_code = process.wait(timeout=5)
    stdout_text = "".join(output_lines)
    success_count, failed_count, status = count_result(stdout_text)
    if return_code != 0:
        status = "rpa_failed"
    return stdout_text, success_count, failed_count, status


def process_once(server_url: str, executor_id: str, rpa_dir: Path, work_dir: Path, no_publish: bool) -> bool:
    flush_pending_results(server_url, work_dir)
    write_executor_status(work_dir, executor_id, "polling", "正在检查待上货任务")
    claim = request_json("POST", absolute_url(server_url, "/api/executor/tasks/claim"), {"executor_id": executor_id, "version": "0.2.0"})
    if not claim.get("task"):
        print("暂无待上货任务")
        write_executor_status(work_dir, executor_id, "idle", "暂无待上货任务")
        return False

    task = claim["task"]
    task_id = int(task["id"])
    print(f"领取任务 #{task_id}: {task.get('name', '')}")
    write_executor_status(work_dir, executor_id, "running", f"正在执行任务 #{task_id}", task_id)
    request_json("POST", absolute_url(server_url, f"/api/executor/tasks/{task_id}/heartbeat"), {"executor_id": executor_id})

    export_url = absolute_url(server_url, claim.get("export_download_url", ""))
    filename = safe_xlsx_filename(claim, task_id, export_url)
    xlsx_path = download_file(export_url, work_dir / "downloads" / filename)
    print(f"下载导入表: {xlsx_path}")

    try:
        stdout_text, success_count, failed_count, status = run_rpa(rpa_dir, xlsx_path, claim.get("manifest", {}), no_publish=no_publish)
        run_log = f"Windows executor finished task {task_id}: {status}"
    except Exception as exc:
        stdout_text = repr(exc)
        success_count = 0
        failed_count = 1
        status = "rpa_failed"
        run_log = f"Windows executor exception: {exc}"
    failure_stage = ""
    failure_reason = ""
    evidence_path = ""
    if status != "rpa_success":
        failure_stage, failure_reason, evidence_path = summarize_failure(stdout_text, run_log)

    report_payload = {
        "executor_id": executor_id,
        "status": status,
        "success_count": success_count,
        "failed_count": failed_count,
        "run_log": run_log,
        "stdout": stdout_text[-50000:],
        "failure_stage": failure_stage,
        "failure_reason": failure_reason,
        "evidence_path": evidence_path,
    }
    try:
        request_json("POST", absolute_url(server_url, f"/api/executor/tasks/{task_id}/report"), report_payload, timeout=120)
        print(f"已回传任务 #{task_id}: {status}")
        write_executor_status(work_dir, executor_id, "idle", f"任务 #{task_id} 已回传: {status}")
    except (urllib.error.URLError, TimeoutError) as exc:
        result_path = write_pending_result(work_dir, task_id, {"task_id": task_id, "report": report_payload, "error": repr(exc)})
        print(f"回传失败，已保存本地结果等待补传: {result_path}")
        write_executor_status(work_dir, executor_id, "report_pending", f"任务 #{task_id} 回传失败，等待补传", task_id)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll server upload tasks and run local Windows RPA.")
    parser.add_argument("--server", default="http://124.156.175.191", help="Server URL")
    parser.add_argument("--executor-id", default=f"windows-{socket.gethostname()}", help="Executor ID")
    parser.add_argument("--rpa-dir", default=str(DEFAULT_RPA_DIR), help="Local RPA project directory")
    parser.add_argument("--work-dir", default=str(executable_dir() / "data" / "executor"), help="Local executor work directory")
    parser.add_argument("--poll", type=int, default=5, help="Poll interval seconds")
    parser.add_argument("--once", action="store_true", help="Run one poll cycle and exit")
    parser.add_argument("--publish", action="store_true", help="Actually publish. Default keeps --no-publish for safety.")
    args = parser.parse_args()

    server_url = normalize_server_url(args.server)
    work_dir = Path(args.work_dir)
    stack, log_file, log_path = setup_executor_logging(work_dir)
    with stack:
        stack.callback(log_file.close)
        with contextlib.redirect_stdout(TeeOutput(sys.__stdout__, log_file)), contextlib.redirect_stderr(TeeOutput(sys.__stderr__, log_file)):
            print(f"\n=== Executor started {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
            print(f"日志文件: {log_path}")
            rpa_dir = resolve_rpa_dir(args.rpa_dir)
            print(f"使用 RPA 目录: {rpa_dir}")
            write_executor_status(work_dir, args.executor_id, "started", "执行器已启动")

            while True:
                try:
                    process_once(server_url, args.executor_id, rpa_dir, work_dir, no_publish=not args.publish)
                except (urllib.error.URLError, TimeoutError) as exc:
                    print(f"连接服务器失败: {exc}")
                    write_executor_status(work_dir, args.executor_id, "server_unreachable", f"连接后台失败: {exc}")
                except Exception as exc:
                    print(f"执行器异常: {type(exc).__name__}: {exc}")
                    write_executor_status(work_dir, args.executor_id, "failed", f"执行器异常: {type(exc).__name__}: {exc}")
                    raise
                if args.once:
                    break
                time.sleep(max(args.poll, 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
