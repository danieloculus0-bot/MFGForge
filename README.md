# MFGForge

MFGForge is a practical manufacturing ERP foundation for small and mid-size fabrication and contract manufacturing shops.

It is built around QCDSM: Quality, Cost, Delivery, Safety, and Morale.

The intent is not to build a toy dashboard. MFGForge is being shaped into a real manufacturing system with durable records, traceable workflows, editable master data, review gates, privacy-safe operational metrics, and human-approved AI assistance.

## Current state

MFGForge currently runs as a Flask + SQLite ERP shell with a dark manufacturing-focused UI, durable schema, generic record screens, linked select fields, smoke-test coverage, and GitHub Actions verification.

The app starts empty. No fake customer, shop, quality, attendance, or quote data is seeded into the system.

## Functional areas

### Master data

- Customers
- Suppliers
- Departments
- Reason codes

### Operating model

- Operating profiles for JIT, hybrid, or inventory-buffered shops
- Planning horizon
- Inventory target days
- Purchasing review cadence
- Lead-time strategy notes

### Production

- Parts
- Work orders
- Customer/part/work-order linkage

### Quality

- RMA, NCR, DMR, CAPA, inspection reject, and customer complaint records
- Deviation requests
- FPY summaries
- Customer-linked, part-linked, and work-order-linked quality history

### Documents and maintenance

- Document control foundation
- Preventive maintenance asset records

### Morale and operational strain

- Aggregate department-level morale snapshots
- Overtime hours
- PTO exhaustion counts
- Unscheduled absence counts
- Unpaid time off counts
- Turnover counts
- Staffing notes and quality-risk notes

### Quoting and BOM review

- Approved supplier/material catalog
- Customer quote intake records
- Drawing reference capture
- PDF BOM candidate records
- BOM review gate before use
- Quote material assignment drafts
- Material cost, standard length, pieces required, and lead-time estimates

### Planning and purchasing

- Planning watchlists
- Lead-time risk watchlists
- Purchasing watchlists
- Supplier/material risk signals
- Required action tracking

### Performance and dashboard metrics

- Operator efficiency baselines
- Quoting throughput baselines
- Dashboard metric snapshots
- FPY and production performance summaries

## AI direction

AI assistance in MFGForge is intended to act like GPS, not a self-driving car.

It may analyze, summarize, draft, recommend, flag risk, extract BOM candidates for review, and prepare reports from approved data.

Human approval is required before business-critical actions such as closing quality records, changing inventory, releasing jobs, approving deviations, approving BOM reviews, assigning quote materials, or sending external communications.

## Repository layout

```text
AGENTS.md                         Agent/workflow rules for this repo
MFGFORGE_MODULE_BLUEPRINT.md       Functional scope and implementation direction
README.md                         Project overview
app.py                            Flask app, UI shell, routes, and module metadata
schema.sql                        Durable SQLite schema
smoke_test.py                     End-to-end smoke coverage for module screens and linked records
requirements.txt                  Runtime dependencies
.github/workflows/smoke-test.yml  GitHub Actions smoke test
```

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app run
```

Optional environment variables:

```powershell
$env:MFGFORGE_SECRET_KEY = "replace-this-before-deployment"
$env:MFGFORGE_DATABASE = "C:\\path\\to\\mfgforge.sqlite"
$env:MFGFORGE_ENV = "development"
```

## Smoke test

```powershell
python smoke_test.py
```

GitHub Actions also runs the smoke test on pushes and pull requests to `main`.

## Data privacy

Do not commit proprietary customer drawings, real RMA events, customer names, defect logs, quote PDFs, private Excel trackers, exports, local databases, attendance data, or company-private records.

Morale and attendance metrics must remain aggregate-only by department, role group, or period unless a compliant internal data model is explicitly approved.

## Development standard

Every feature should move the product closer to deployable ERP software.

A valid feature should have at least one of the following:

- durable schema
- usable screen or route
- clear record workflow
- traceable review/approval path
- smoke-test coverage
- dashboard/reporting value

Avoid mockup theater, fake records, placeholder modules, and disconnected UI panels that do not create useful manufacturing records.
