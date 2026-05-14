$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

Write-Host "=== MFGForge venv runtime verification ==="

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "=== Launcher health check ==="
& .\.venv\Scripts\python.exe .\mfgforge_launcher.py --health-check

Write-Host "=== Import and route verification ==="
& .\.venv\Scripts\python.exe -c "from app import create_app, MODULES; app=create_app({'TESTING': True, 'DATABASE': 'instance/runtime_verify.sqlite'}); c=app.test_client(); paths=['/','/company-pulse','/ai-policy','/records/material-certificates/new']; failed=[(p,c.get(p).status_code) for p in paths if c.get(p).status_code != 200]; assert not failed, failed; print('verified modules:', len(MODULES))"

Write-Host "MFGForge runtime verification passed."
