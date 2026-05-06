param(
  [switch]$Clean,
  [switch]$SkipInstall
)

$ErrorActionPreference = 'Stop'
$Root = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $Root

$Python = Join-Path $Root '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) {
  $Python = 'python'
}

if (-not $SkipInstall) {
  & $Python -m pip install -r requirements.txt -r requirements-build.txt
  if ($LASTEXITCODE -ne 0) { throw '依赖安装失败' }
}

if ($Clean) {
  Remove-Item -LiteralPath (Join-Path $Root 'build') -Recurse -Force -ErrorAction SilentlyContinue
  Remove-Item -LiteralPath (Join-Path $Root 'dist\upload-assistant-backend') -Recurse -Force -ErrorAction SilentlyContinue
}

& $Python -m PyInstaller backend\upload_assistant_backend.spec --noconfirm
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller 打包失败' }

$DistDir = Join-Path $Root 'dist\upload-assistant-backend'
$DataDir = Join-Path $DistDir 'data'
New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $DataDir 'images') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $DataDir 'export') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $DataDir 'logs') -Force | Out-Null

$Launcher = @"
@echo off
setlocal
set UPLOAD_ASSISTANT_HOST=127.0.0.1
set UPLOAD_ASSISTANT_PORT=8000
set UPLOAD_ASSISTANT_OPEN_BROWSER=true
set UPLOAD_ASSISTANT_BROWSER_URL=http://124.156.175.191
""%~dp0upload-assistant-backend.exe""
pause
"@
Set-Content -LiteralPath (Join-Path $DistDir '启动上货助手后台.bat') -Value $Launcher -Encoding UTF8

Write-Host "打包完成：$DistDir" -ForegroundColor Green
Write-Host "启动：$DistDir\启动上货助手后台.bat" -ForegroundColor Green
