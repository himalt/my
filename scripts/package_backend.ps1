param(
  [switch]$Clean,
  [switch]$SkipInstall
)

$ErrorActionPreference = 'Stop'
$Root = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $Root

$BuiltinApiConfig = Join-Path $Root 'config\builtin_api_configs.json'
if (-not (Test-Path $BuiltinApiConfig)) {
  Write-Warning '未找到 config\builtin_api_configs.json；本次包不会内置真实 API Key，客户需要手动填写或使用本地兜底标题。'
}

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

& $Python -m PyInstaller scripts\windows_executor.py --name upload-assistant-executor --distpath dist\executor-build --workpath build\executor-build --specpath build\executor-build --onefile --console --noconfirm
if ($LASTEXITCODE -ne 0) { throw '执行器打包失败' }

& $Python -m PyInstaller rpa\rpa_upload.py --name rpa_upload --distpath dist\rpa-build --workpath build\rpa-build --specpath build\rpa-build --onefile --console --paths rpa --hidden-import playwright.sync_api --hidden-import pipeline --noconfirm
if ($LASTEXITCODE -ne 0) { throw 'RPA 打包失败' }

$DistDir = Join-Path $Root 'dist\upload-assistant-backend'
$DataDir = Join-Path $DistDir 'data'
$DataSubdirs = @('images', 'export', 'logs', 'collection_requests', 'collection_results', 'imports', 'templates', 'uploads', 'rpa_images')
New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
Remove-Item -LiteralPath (Join-Path $DataDir 'app.db') -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $DataDir 'app.db-shm') -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $DataDir 'app.db-wal') -Force -ErrorAction SilentlyContinue
foreach ($Name in $DataSubdirs) {
  New-Item -ItemType Directory -Path (Join-Path $DataDir $Name) -Force | Out-Null
}

Copy-Item -LiteralPath (Join-Path $Root 'scripts\windows_executor.py') -Destination (Join-Path $DistDir 'windows_executor.py') -Force
Copy-Item -LiteralPath (Join-Path $Root 'dist\executor-build\upload-assistant-executor.exe') -Destination (Join-Path $DistDir 'upload-assistant-executor.exe') -Force
$RpaSourceDir = Join-Path $Root 'rpa'
$RpaDistDir = Join-Path $DistDir 'rpa'
if (Test-Path $RpaSourceDir) {
  Remove-Item -LiteralPath $RpaDistDir -Recurse -Force -ErrorAction SilentlyContinue
  New-Item -ItemType Directory -Path $RpaDistDir -Force | Out-Null
  Copy-Item -LiteralPath (Join-Path $Root 'dist\rpa-build\rpa_upload.exe') -Destination (Join-Path $RpaDistDir 'rpa_upload.exe') -Force
  Copy-Item -LiteralPath (Join-Path $RpaSourceDir 'rpa_upload.py') -Destination (Join-Path $RpaDistDir 'rpa_upload.py') -Force
  if (Test-Path (Join-Path $RpaSourceDir 'pipeline.py')) {
    Copy-Item -LiteralPath (Join-Path $RpaSourceDir 'pipeline.py') -Destination (Join-Path $RpaDistDir 'pipeline.py') -Force
  }
  $PlaywrightCache = $env:PLAYWRIGHT_BROWSERS_PATH
  if (-not $PlaywrightCache) { $PlaywrightCache = Join-Path $env:LOCALAPPDATA 'ms-playwright' }
  if (Test-Path $PlaywrightCache) {
    $PlaywrightDist = Join-Path $RpaDistDir 'ms-playwright'
    Remove-Item -LiteralPath $PlaywrightDist -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $PlaywrightDist -Force | Out-Null
    Get-ChildItem -LiteralPath $PlaywrightCache -Directory | Where-Object { $_.Name -match '^(chromium|chromium_headless_shell|ffmpeg|winldd)-' } | ForEach-Object {
      Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $PlaywrightDist $_.Name) -Recurse -Force
    }
  } else {
    Write-Warning '未找到本机 Playwright 浏览器缓存；客户电脑可能仍需安装 Playwright 浏览器。'
  }
}


$LauncherLines = @(
  '@echo off',
  'chcp 65001 >nul',
  'setlocal',
  'cd /d "%~dp0"',
  'set "UPLOAD_ASSISTANT_HOST=127.0.0.1"',
  'set "UPLOAD_ASSISTANT_PORT=8000"',
  'set "UPLOAD_ASSISTANT_OPEN_BROWSER=true"',
  'set "UPLOAD_ASSISTANT_DATA_DIR=%~dp0data"',
  'set "UPLOAD_ASSISTANT_DB=%~dp0data\app.db"',
  'if not exist "data\logs" mkdir "data\logs"',
  'start "Upload Assistant" /min "%~dp0upload-assistant-backend.exe"',
  'timeout /t 3 /nobreak >nul',
  'if exist "%~dp0upload-assistant-executor.exe" start "Upload Executor" /min "%~dp0upload-assistant-executor.exe" --server http://127.0.0.1:8000 --work-dir "%~dp0data\executor" --publish',
  'exit /b 0'
)
$Launcher = [string]::Join("`r`n", $LauncherLines) + "`r`n"
[System.IO.File]::WriteAllText((Join-Path $DistDir 'start-assistant.bat'), $Launcher, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText((Join-Path $DistDir '启动上货助手.bat'), $Launcher, [System.Text.UTF8Encoding]::new($false))

$ExecutorLauncherLines = @(
  '@echo off',
  'chcp 65001 >nul',
  'setlocal',
  'cd /d "%~dp0"',
  'if not exist "data\logs" mkdir "data\logs"',
  'echo [%date% %time%] ??????? > "data\logs\executor-launch.log"',
  'echo ?????%cd% >> "data\logs\executor-launch.log"',
  'if exist "%~dp0upload-assistant-executor.exe" (',
  '  echo ?????????...',
  '  "%~dp0upload-assistant-executor.exe" --server http://127.0.0.1:8000 --publish 2>&1',
  ') else (',
  '  where python >> "data\logs\executor-launch.log" 2>&1',
  '  if errorlevel 1 (',
  '    echo ??? Python???? upload-assistant-executor.exe????????????? >> "data\logs\executor-launch.log"',
  '    echo ??? Python???? upload-assistant-executor.exe?????????????',
  '    pause',
  '    exit /b 1',
  '  )',
  '  echo ???? Python ???...',
  '  python "%~dp0windows_executor.py" --server http://127.0.0.1:8000 --publish 2>&1',
  ')',
  'echo ??????????%~dp0data\logs\executor-launch.log',
  'pause'
)
$ExecutorLauncher = [string]::Join("`r`n", $ExecutorLauncherLines) + "`r`n"
[System.IO.File]::WriteAllText((Join-Path $DistDir 'start-executor.bat'), $ExecutorLauncher, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText((Join-Path $DistDir '启动上货执行器.bat'), $ExecutorLauncher, [System.Text.UTF8Encoding]::new($false))

$Readme = @"
上货助手 本地客户端
====================

1. 双击「启动上货助手.bat」打开本地页面。
2. 数据保存在当前目录 data\，包括数据库、图片、导出表和日志。
3. 执行器会自动启动并领取任务，页面顶部会显示执行器在线/离线。
4. 真实采集需要在页面设置万邦 Key/Secret 或 1688 Cookie。
5. 真实上货前请在页面填写店铺与模板信息。

本地地址：http://127.0.0.1:8000
日志目录：data\logs
"@
Set-Content -LiteralPath (Join-Path $DistDir 'README-本地客户端.txt') -Value $Readme -Encoding UTF8

$ReleaseDir = Join-Path $Root 'release'
New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null
$ZipPath = Join-Path $ReleaseDir 'upload-assistant-local-client.zip'
Remove-Item -LiteralPath $ZipPath -Force -ErrorAction SilentlyContinue
Compress-Archive -Path (Join-Path $DistDir '*') -DestinationPath $ZipPath -Force

Write-Host "打包完成：$DistDir" -ForegroundColor Green
Write-Host "启动：$DistDir\启动上货助手.bat" -ForegroundColor Green
Write-Host "压缩包：$ZipPath" -ForegroundColor Green
