from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

APP_NAME = "上货助手"
ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "version.json"
DATA_DIR = ROOT / "data"
LOG_DIR = DATA_DIR / "logs"
DEFAULT_MANIFEST_NAME = "update-manifest.json"
PRESERVE_NAMES = {"data", "version.json"}
PRESERVE_SUFFIXES = {".db", ".sqlite", ".sqlite3"}


def log(message: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(line)
    with (LOG_DIR / "updater.log").open("a", encoding="utf-8", errors="replace") as file:
        file.write(line + "\n")


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def current_version() -> str:
    return str(read_json(VERSION_FILE).get("version") or "0.0.0")


def version_tuple(value: str) -> tuple[int, ...]:
    parts: list[int] = []
    for part in str(value).replace("-", ".").split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        parts.append(int(digits or 0))
    return tuple(parts or [0])


def is_newer(remote: str, local: str) -> bool:
    return version_tuple(remote) > version_tuple(local)


def fetch_manifest(source: str) -> dict:
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=20) as response:
            return json.loads(response.read().decode("utf-8-sig"))
    return read_json(Path(source))


def download_file(url: str, target: Path) -> None:
    if url.startswith(("http://", "https://")):
        with urllib.request.urlopen(url, timeout=120) as response, target.open("wb") as file:
            shutil.copyfileobj(response, file)
        return
    shutil.copyfile(Path(url), target)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stop_running_processes() -> None:
    if os.name != "nt":
        return
    names = {"upload-assistant-backend.exe", "upload-assistant-executor.exe", "rpa_upload.exe"}
    for name in names:
        subprocess.run(["taskkill", "/F", "/IM", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def backup_current() -> Path:
    backup_root = DATA_DIR / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    backup_dir = backup_root / f"app_before_update_{time.strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for item in ROOT.iterdir():
        if item.name in {"data", ".git", "build", "dist", "release"}:
            continue
        target = backup_dir / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)
    return backup_dir


def should_preserve(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    first = relative.parts[0] if relative.parts else path.name
    return first in PRESERVE_NAMES or path.suffix.lower() in PRESERVE_SUFFIXES


def copy_update_payload(extracted_root: Path) -> None:
    candidates = [extracted_root]
    child_dirs = [item for item in extracted_root.iterdir() if item.is_dir()]
    if len(child_dirs) == 1:
        candidates.insert(0, child_dirs[0])
    source_root = next((candidate for candidate in candidates if (candidate / "启动上货助手.bat").exists() or (candidate / "upload-assistant-backend.exe").exists()), candidates[0])
    for item in source_root.iterdir():
        target = ROOT / item.name
        if should_preserve(target):
            continue
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def apply_update(manifest: dict) -> bool:
    local = current_version()
    remote = str(manifest.get("version") or "")
    if not remote:
        raise RuntimeError("更新清单缺少 version")
    if not is_newer(remote, local):
        log(f"当前已是最新版本：{local}")
        return False
    url = str(manifest.get("url") or "")
    if not url:
        raise RuntimeError("更新清单缺少 url")
    with tempfile.TemporaryDirectory(prefix="upload_assistant_update_") as temp:
        temp_dir = Path(temp)
        package_path = temp_dir / "update.zip"
        log(f"发现新版本 {remote}，开始下载")
        download_file(url, package_path)
        expected_hash = str(manifest.get("sha256") or "").strip().lower()
        if expected_hash:
            actual_hash = sha256_file(package_path)
            if actual_hash.lower() != expected_hash:
                raise RuntimeError(f"更新包校验失败：{actual_hash}")
        extract_dir = temp_dir / "extract"
        with zipfile.ZipFile(package_path) as archive:
            archive.extractall(extract_dir)
        stop_running_processes()
        backup = backup_current()
        log(f"已备份当前版本：{backup}")
        copy_update_payload(extract_dir)
        version_data = read_json(VERSION_FILE)
        version_data.update({
            "version": remote,
            "channel": manifest.get("channel") or version_data.get("channel") or "stable",
            "update_url": manifest.get("manifest_url") or version_data.get("update_url") or "",
            "notes": manifest.get("notes") or "",
        })
        write_json(VERSION_FILE, version_data)
        log(f"更新完成：{local} -> {remote}")
        return True


def default_manifest_source() -> str:
    version_data = read_json(VERSION_FILE)
    return str(version_data.get("update_url") or ROOT / DEFAULT_MANIFEST_NAME)


def main() -> int:
    parser = argparse.ArgumentParser(description=f"{APP_NAME} 自动更新器")
    parser.add_argument("--manifest", default=default_manifest_source(), help="更新清单 URL 或本地路径")
    parser.add_argument("--check", action="store_true", help="只检查不安装")
    args = parser.parse_args()
    manifest = fetch_manifest(args.manifest)
    local = current_version()
    remote = str(manifest.get("version") or "")
    if args.check:
        if remote and is_newer(remote, local):
            print(json.dumps({"update_available": True, "current": local, "latest": remote}, ensure_ascii=False))
            return 2
        print(json.dumps({"update_available": False, "current": local, "latest": remote or local}, ensure_ascii=False))
        return 0
    apply_update(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
