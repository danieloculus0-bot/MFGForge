# SuperForge Replit Demo

## Purpose

This is a lightweight demo launch path for SuperForge while the Windows executable path continues separately.

It runs the same SuperForge wrapper used by the local launcher:

```text
superforge_app.create_superforge_app()
```

## Replit launch

Import the GitHub repo into Replit:

```text
https://github.com/danieloculus0-bot/MFGForge
```

Replit should detect:

```text
.replit
main.py
requirements.txt
```

Click Run.

The app starts with:

```text
python main.py
```

## Optional verification before Run

In the Replit Shell:

```bash
python scripts/verify_replit_demo.py
```

Expected output:

```text
SuperForge Replit demo verification passed.
```

## Runtime behavior

The demo binds to:

```text
0.0.0.0:$PORT
```

If `PORT` is not provided, it falls back to:

```text
5000
```

The demo database is created at:

```text
instance/superforge_replit_demo.sqlite
```

## Demo routes to verify

Open these after launch:

```text
/
/company-pulse
/intelligence
/workflows/quote-lead-time-review
/workflows/material-cert-review
/records/customers
/records/material-certificates/new
/records/machine-utilization/new
/records/supplier-performance/new
/records/quote-intakes/new
```

## Important notes

Do not upload real company data, customer drawings, cert files, quote PDFs, RMA data, attendance data, or private shop records to the Replit demo.

This is for functional demo/testing only.

The Windows packaging path remains:

```powershell
.\scripts\verify_runtime.ps1
.\scripts\build_windows_exe.ps1
```

Expected executable output:

```text
dist\SuperForge.exe
```
