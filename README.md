# MFGForge / SuperForge ERP Suite

MFGForge is the source-of-truth application repo for the SuperForge ERP Suite: a local-first manufacturing ERP foundation for small and mid-size fabrication, machining, contract manufacturing, and job-shop environments.

The project is built around QCDSM: Quality, Cost, Delivery, Safety, and Morale. The goal is not a toy dashboard or a loose pile of disconnected forms. The goal is a practical, deployable manufacturing system with durable records, traceable workflows, editable master data, review gates, privacy-safe operational metrics, and human-approved intelligence across quality, quoting, purchasing, planning, maintenance, documents, and management reporting.

SuperForge is intended to feel closer to a focused shop-floor ERP and quality command center than a bloated enterprise system. It should help a small manufacturer see what is happening, why it matters, what is at risk, and what needs human action.

## Current project status

MFGForge currently runs as a Flask + SQLite ERP shell with:

- dark manufacturing-focused UI
- durable SQLite schema
- generic record screens
- linked select fields
- module-style navigation
- Company Pulse / operational risk direction
- quote intake and BOM review foundation
- material and supplier foundations
- quality event and deviation foundations
- machine and PM asset foundations
- privacy-safe morale and operational strain concepts
- smoke-test coverage
- GitHub Actions verification

The app starts empty. No fake customer, shop, quality, attendance, maintenance, quote, supplier, or production data is seeded into the system.

## Repository roles

| Repo or system | Role |
| --- | --- |
| `danieloculus0-bot/MFGForge` | Primary source repo and integration host for the SuperForge ERP application. |
| `danieloculus0-bot/ForgeQC` | Quality and quoting intelligence source project to audit and selectively absorb. |
| `danieloculus0-bot/ForgeVault` | Vendor, purchased part, material, supplier, document, and traceability source project to audit and selectively absorb. |
| PM Tracking | Behavioral reference for the future native preventive maintenance module. It will not be copied as source. |
| `danieloculus0-bot/SuperForge_Unofficial` | Build artifact and unofficial distribution repo for compiled outputs, release candidates, manifests, checksums, packaging notes, and installer experiments. |

MFGForge remains the canonical source repo. SuperForge_Unofficial is for packaged artifacts and release-candidate outputs, not the main application source.

## Suite vision

SuperForge is being shaped into a manufacturing suite with the following major areas.

### Core ERP foundation

Core provides the shared application structure and records that every other module depends on:

- local Flask runtime
- SQLite database
- app factory direction
- shared navigation
- shared layout
- shared module registry
- audit helpers
- editable master data
- customers, suppliers, departments, parts, work orders, reason codes, and operating profiles

This core layer should stay boring, durable, and dependable. Every flashy module still has to land on clean records and traceable database behavior.

### Quality management

The quality side is intended to cover the practical daily work of a Quality Engineer in a job-shop or contract manufacturing environment:

- RMA tracking
- NCR records
- DMR records
- CAPA workflow
- deviation requests
- inspection rejects
- customer complaints
- containment, root cause, corrective action, owner, due date, and closure tracking
- customer-linked, part-linked, and work-order-linked quality history
- editable reason codes
- defect trend reporting
- FPY summaries
- management review support

ForgeQC is the source project to audit for deeper quality workflow behavior before migration. MFGForge already has the anchor concepts through `quality_events`, `deviations`, `reason_codes`, `fpy_summaries`, customers, parts, and work orders.

### Vendor, material, and document vault

The vault side is meant to control the messy records that usually scatter across emails, PDFs, downloads, vendor pages, and local folders:

- supplier records
- purchased/vendor part records
- approved material records
- controlled document references
- material certificate references
- heat/lot traceability direction
- document metadata
- drawing/spec/procedure references
- vendor intake patterns such as McMaster-style purchased part entry

ForgeVault is the source project to audit for reusable vendor, purchased-part, material, and document-control behavior. MFGForge owns the ERP identity and linkage. ForgeVault contributes proven intake and vault patterns after inspection.

### Preventive maintenance and machine readiness

PM will be rebuilt natively inside MFGForge/SuperForge as `modules/pm`. The existing PM Tracking app is a behavioral reference only, not source code to copy into the ERP.

Reference behavior from the old PM Tracking app includes:

- machine status cards
- machine detail pages
- manual operator PM completion entry
- printable SVG QR labels
- QR Codes page
- Excel export
- Flask + openpyxl + sqlite3 workflow
- future maintenance ticket form direction

The native PM module should eventually include:

- machine and equipment asset records
- PM schedules
- PM completion history
- maintenance tickets
- secure QR label workflow
- machine readiness status
- overdue PM risk signals
- planning and capacity risk inputs
- Company Pulse maintenance signals
- controlled Excel import/export where appropriate

PM data such as `pm_data.xlsx`, `pm_app.db`, machine history, employee-level records, exports, and shop-private maintenance records must not be committed.

### Quoting and BOM review

The quoting side is meant to reduce the chaos around customer drawings, quote requests, BOM guesses, material assignments, and lead-time assumptions:

- customer quote intake
- drawing reference capture
- customer requirement capture
- PDF BOM candidate records
- human BOM review gate before use
- quote material assignment drafts
- approved supplier/material catalog
- material cost estimates
- standard length and pieces-required estimates
- lead-time assumptions
- supplier and machine capacity risk signals feeding quote confidence

AI or automation may help extract and draft BOM candidates, but extracted candidates must remain reviewable records. Nothing from a PDF should silently become approved quoting truth.

### Planning and purchasing

Planning and purchasing are intended to expose risk before it burns the shop down:

- planning watchlists
- purchasing watchlists
- work-order risk signals
- supplier lead-time risk
- material availability risk
- machine capacity pressure
- machine readiness / PM risk
- buyer-owner tracking
- action-required tracking
- quote lead-time confidence inputs

The planning goal is not full MRP magic on day one. The first goal is visibility: what is at risk, who owns it, and what needs action.

### Intelligence and Company Pulse

Company Pulse is the cross-module risk lens. It should combine quality, supplier, purchasing, planning, quoting, machine readiness, FPY, and aggregate morale indicators into useful operational signals.

Possible signal areas include:

- open quality events
- open deviations
- material certificates needing review
- quote/BOM review backlog
- supplier lead-time pressure
- high-risk purchasing watchlist items
- high-risk planning watchlist items
- machine capacity pressure
- overdue PMs
- machines down or limited-use
- aggregate morale and staffing strain
- FPY trends

The point is not to replace managers or supervisors. The point is to make hidden risk visible early enough for humans to act.

### Reporting

Reporting should support practical shop and management needs:

- management review summaries
- KPI snapshots
- FPY summaries
- RMA/NCR/DMR/CAPA trends
- supplier performance summaries
- quote throughput summaries
- planning and purchasing risk summaries
- PM readiness and overdue summaries
- Company Pulse summaries

Reports should be professional and grounded in actual records. No fake data, no filler metrics, and no disconnected dashboard theater.

## AI direction

AI assistance in SuperForge is intended to act like GPS, not a self-driving car.

It may:

- summarize records
- draft recommendations
- flag risks
- extract BOM candidates for human review
- prepare quality summaries
- prepare management review support
- identify trend clusters
- suggest follow-up actions
- help explain why a record appears risky

It must not silently approve or execute:

- BOM approvals
- material assignment approvals
- material certificate approvals
- deviation approvals
- quality event closures
- quote releases
- shipment readiness decisions
- purchasing actions
- PM closures
- machine readiness releases
- customer-facing communications
- employee-level morale or performance decisions

Business-critical AI suggestions must remain reviewable, approval-gated, and traceable.

## Functional areas currently represented

### Master data

- customers
- suppliers
- departments
- reason codes

### Operating model

- operating profiles for JIT, hybrid, or inventory-buffered shops
- planning horizon
- inventory target days
- purchasing review cadence
- lead-time strategy notes

### Production

- parts
- work orders
- customer/part/work-order linkage
- machine assets
- machine utilization snapshots

### Quality

- quality events for RMA, NCR, DMR, CAPA, rejects, and complaints
- deviation requests
- FPY summaries
- customer-linked, part-linked, and work-order-linked quality history

### Documents, materials, and certificates

- document control foundation
- approved materials
- material certificate control
- supplier linkage
- work-order linkage
- heat/lot reference direction
- storage references
- review status

### Maintenance

- PM asset foundation
- native PM rebuild planning
- future PM schedules, completion history, QR labels, maintenance tickets, and machine readiness signals

### Morale and operational strain

- aggregate department-level morale snapshots
- overtime hours
- PTO exhaustion counts
- unscheduled absence counts
- unpaid time off counts
- turnover counts
- staffing notes
- quality-risk notes

Morale and attendance indicators must remain aggregate-only unless a compliant internal data model is explicitly approved.

### Quoting and BOM review

- approved supplier/material catalog
- customer quote intake records
- drawing reference capture
- PDF BOM candidate records
- BOM review gate before use
- quote material assignment drafts
- material cost, standard length, pieces required, and lead-time estimates

### Supplier intelligence

- supplier performance snapshots
- quoted lead time versus actual average lead time
- late delivery counts
- supplier quality issue counts
- risk level
- impact notes

### Planning and purchasing

- planning watchlists
- lead-time risk watchlists
- purchasing watchlists
- supplier/material risk signals
- required action tracking

### Performance and dashboard metrics

- operator or group efficiency baselines
- quoting throughput baselines
- dashboard metric snapshots
- FPY and production performance summaries

## Planning documents

Current suite-planning documents include:

- `SUPERFORGE_REPO_AUDIT.md` - source-system roles, reusable logic, conflicts, and risk notes
- `SUPERFORGE_INTEGRATION_MAP.md` - target architecture, module mapping, safest migration sequence, and source ownership decisions
- `PM_NATIVE_REBUILD_SPEC.md` - native PM rebuild plan using the old PM Tracking app as behavioral reference only

## Repository layout

```text
AGENTS.md                         Workflow rules for this repo
MFGFORGE_MODULE_BLUEPRINT.md       Functional scope and implementation direction
README.md                         Project overview
SUPERFORGE_REPO_AUDIT.md           SuperForge source-system audit
SUPERFORGE_INTEGRATION_MAP.md      SuperForge integration map
PM_NATIVE_REBUILD_SPEC.md          Native PM rebuild plan
app.py                            Flask app, UI shell, routes, and module metadata
main.py                           Hosted Python/Replit entrypoint for the real SuperForge app
superforge_app.py                  SuperForge wrapper around the MFGForge app
schema.sql                        Durable SQLite schema
smoke_test.py                     End-to-end smoke coverage for module screens and linked records
scripts/verify_hosted_runtime.py  Replit/browser-hosted runtime verification
requirements.txt                  Runtime dependencies
.github/workflows/smoke-test.yml  GitHub Actions smoke and hosted runtime checks
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

## Run SuperForge locally

```powershell
python main.py
```

`main.py` launches the real SuperForge Flask app through `superforge_app.create_superforge_app`. It does not seed fake data and does not replace the app with a mockup.

## Run in Replit or similar

This runs the Flask source app, not the Windows `.exe`.

Use this command:

```bash
python main.py
```

The hosted runtime binds to `0.0.0.0` and uses the `PORT` environment variable when provided. If no `PORT` is provided, it defaults to `8080`.

The runtime database is created under `instance/superforge.sqlite` unless `MFGFORGE_DATABASE` is set. Do not commit runtime databases.

## Windows executable build

The Windows executable is built separately from the hosted web runtime.

```powershell
.\scripts\build_windows_exe.ps1
```

Expected packaged output:

```text
dist\SuperForge.exe
```

Build outputs belong in `SuperForge_Unofficial` or a release artifact flow, not as normal source files in MFGForge.

## Smoke test

```powershell
python smoke_test.py
python scripts/verify_hosted_runtime.py
```

GitHub Actions also runs the smoke test and hosted runtime verification on pushes and pull requests to `main`.

## Data privacy

Do not commit:

- proprietary customer drawings
- real RMA events
- real customer names or customer records
- defect logs from private operations
- quote PDFs
- private Excel trackers
- runtime exports
- local databases
- attendance data
- employee-level morale records
- material cert files
- PM databases such as `pm_app.db`
- PM spreadsheets such as `pm_data.xlsx`
- machine maintenance history from the shop
- company-private records

Keep source code, schema, sanitized docs, tests, and clean examples separate from operational data.

## Development standard

Every feature should move the product closer to deployable ERP software.

A valid feature should have at least one of the following:

- durable schema
- usable screen or route
- clear record workflow
- traceable review/approval path
- smoke-test coverage
- dashboard/reporting value
- controlled import/export behavior
- privacy-safe risk signal

Avoid mockup theater, fake records, placeholder modules, and disconnected UI panels that do not create useful manufacturing records.

## Near-term direction

Recommended next steps:

1. Merge documentation-only planning PRs cleanly.
2. Audit ForgeQC file-by-file before importing quality workflow logic.
3. Audit ForgeVault file-by-file before importing vault/material/document logic.
4. Add tests around current MFGForge behavior before major refactoring.
5. Reconcile `app.py` registry logic with `module_registry.py`.
6. Build native PM module skeleton only after the PM rebuild spec is accepted.
7. Keep runtime build artifacts in `SuperForge_Unofficial`, not in MFGForge.

SuperForge should grow carefully: one working, traceable, tested manufacturing workflow at a time.