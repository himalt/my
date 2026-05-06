@echo off
setlocal
cd /d %~dp0\..
python scripts\windows_executor.py --server http://124.156.175.191
pause
