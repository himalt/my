@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title 上货助手
if not exist "data\logs" mkdir "data\logs"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
where python >nul 2>nul
if errorlevel 1 (
  echo 未检测到 Python。后续正式安装包会内置运行环境。
  echo 当前源码调试版请先安装 Python，或联系开发打包 EXE。
  pause
  exit /b 1
)
echo 正在启动上货助手...
echo 后台、执行器、页面会自动启动；不要再单独打开执行器。
python "scripts\launcher.py"
if errorlevel 1 (
  echo 启动失败，请查看 data\logs\launcher.log
  pause
)
