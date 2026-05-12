# MFGForge

MFGForge is a practical manufacturing ERP foundation for small and mid-size fabrication and contract manufacturing shops.

It is built around QCDSM: Quality, Cost, Delivery, Safety, and Morale.

## Current foundation

This repository now has a runnable Flask + SQLite ERP shell.

Included modules:

- Customers
- Suppliers
- Departments
- Reason codes
- Parts
- Work orders
- Quality events: RMA, NCR, DMR, CAPA, inspection rejects, customer complaints
- Deviation requests
- Documents
- Preventive maintenance assets
- Aggregate morale snapshots
- AI action log schema

No fake customer, quality, attendance, or shop data is included.

## AI direction

AI assistance in MFGForge is intended to act like GPS, not a self-driving car.

It may analyze, summarize, draft, recommend, and prepare reports. Business-critical execution requires human approval and audit logging.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app run
```

## Smoke test

```powershell
python smoke_test.py
```

GitHub Actions also runs the smoke test on pushes and pull requests to `main`.

## Data privacy

Do not commit proprietary customer drawings, real RMA events, customer names, defect logs, quote PDFs, private Excel trackers, exports, local databases, attendance data, or company-private records.

Morale and attendance metrics must remain aggregate-only by department, role group, or period unless a compliant internal data model is explicitly approved.
