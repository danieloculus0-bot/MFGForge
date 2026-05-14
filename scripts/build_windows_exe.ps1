$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

Write-Host "=== MFGForge Windows package build ==="

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "=== Pre-package runtime health check ==="
& .\.venv\Scripts\python.exe .\mfgforge_launcher.py --health-check

Write-Host "=== Build package ==="
& .\.venv\Scripts\pyinstaller.exe --clean --noconfirm .\MFGForge.spec

$package = Join-Path $repo "dist\MFGForge.exe"
if (-not (Test-Path $package)) {
    throw "Expected package was not created: $package"
}

Write-Host "=== Packaged runtime health check ==="
& $package --health-check

Write-Host "MFGForge package ready: $package"
