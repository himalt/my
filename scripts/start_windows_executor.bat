@echo off
chcp 65001 >nul
setlocal
cd /d %~dp0\..
if not exist "data\logs" mkdir "data\logs"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
python scripts\windows_executor.py --server http://127.0.0.1:8000 --work-dir data\executor --publish
pause
