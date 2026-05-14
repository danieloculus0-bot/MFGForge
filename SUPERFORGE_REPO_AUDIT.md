# SuperForge Repository Audit

Date: 2026-05-14
Target repo: `danieloculus0-bot/MFGForge`
Repair note: this document is intentionally documentation-only. It does not change runtime code, schema, tests, packaging scripts, or build artifacts.

## Scope

This audit maps the current SuperForge source systems and separates source-of-truth application work from build artifact staging.

| Source | Role | Current handling |
| --- | --- | --- |
| `danieloculus0-bot/MFGForge` | Primary ERP source and integration host | Keep as source of truth for the working SuperForge application. |
| `danieloculus0-bot/ForgeQC` | Quality and quoting intelligence source | Inspect for reusable QC workflows before migration. |
| `danieloculus0-bot/ForgeVault` | Vendor, purchased part, material, and document vault source | Inspect for reusable vault and supplier logic before migration. |
| PM Tracking | Preventive maintenance source system | Pending local audit at `C:\Users\dboone\PM Tracking`. |
| `danieloculus0-bot/SuperForge_Unofficial` | Build artifact and unofficial distribution repo | Use for compiled outputs, release candidates, packaging notes, and installer experiments only. |

## MFGForge audit

### Purpose and role

MFGForge is the current SuperForge host application. It should remain the ERP source repo for core Flask code, SQLite schema, module routing, shared navigation, reporting, intelligence governance, and future packaging scripts.

### App entrypoints

- `app.py` - Flask app factory, route registration, module registry, generic record list and create routes, dashboard, Company Pulse, AI policy screen, and database helpers.
- `smoke_test.py` - local smoke test entrypoint.
- `flask --app app run` - documented local development launch pattern.

### Schema and database files

- `schema.sql` is the current durable SQLite schema.
- Existing table families include:
  - master data: `customers`, `suppliers`, `departments`, `reason_codes`, `operating_profiles`
  - production: `parts`, `work_orders`, `machine_assets`, `machine_utilization_snapshots`
  - quality: `quality_events`, `deviations`, `fpy_summaries`
  - documents and certificates: `documents`, `material_certificates`
  - maintenance: `pm_assets`
  - quoting: `materials`, `quote_intakes`, `pdf_bom_candidates`, `bom_reviews`, `quote_material_drafts`
  - supplier and planning: `supplier_performance_snapshots`, `planning_watchlists`, `purchasing_watchlists`
  - performance and pulse: `operator_efficiency_baselines`, `quoting_throughput_baselines`, `dashboard_metric_snapshots`, `morale_snapshots`
  - governance: `ai_action_log`, `system_meta`
- No runtime SQLite database should be committed as source.

### Route files

- MFGForge currently appears centered around `app.py` rather than split route files.
- Current route categories include dashboard, Company Pulse, AI policy, generic module listing, and generic module record creation.
- Future modularization should split routes only after tests protect current behavior.

### Utility modules

- `app.py` contains database helpers, table count helpers, insert helpers, select option loading, and Company Pulse calculation logic.
- `module_registry.py` exists as a related registry concept and must be reconciled with the active registry in `app.py` before major modularization.

### Templates and static assets

- Current UI is largely inline in `app.py` using Flask/Jinja rendering patterns.
- A future refactor should move shared HTML into `templates/` and CSS/JS into `static/`, but not until the current app behavior is test-covered.

### Tests

- `smoke_test.py` is the current safety check.
- It should remain the first guardrail before moving routes, schemas, or registry code.
- More module-specific tests should be added before importing ForgeQC, ForgeVault, or PM Tracking behavior.

### Packaging and runtime files

- `requirements.txt` defines Python dependencies.
- Existing docs such as `README.md`, `AGENTS.md`, and module planning docs should remain in MFGForge.
- Windows executable output belongs in `SuperForge_Unofficial`, not in the MFGForge source tree.

### Reusable native logic

- Generic module registry and record-entry pattern.
- SQLite-first ERP schema.
- Company Pulse risk scoring concept.
- Quoting intake, PDF BOM candidate, BOM review, and material draft concepts.
- Supplier performance, purchasing, planning, machine capacity, FPY, morale, and dashboard snapshot concepts.
- AI governance concept using logged human approval states.

### Duplicate or overlapping concerns

- `app.py` and `module_registry.py` may duplicate registry concepts.
- `quality_events` overlaps with expected ForgeQC RMA, NCR, DMR, CAPA, deviation, and inspection workflows.
- `documents` and `material_certificates` overlap with expected ForgeVault document and cert handling.
- `pm_assets` overlaps with PM Tracking machine asset and PM completion workflows.

### Known risks

- Do not blindly copy external repos into MFGForge.
- Do not commit private records, customer drawings, local databases, Excel trackers, RMA data, cert files, or runtime exports.
- Do not create fake/demo business data to make the suite look integrated.
- Do not let AI silently approve BOMs, certs, deviations, quotes, shipments, purchasing actions, PM closures, machine readiness, or customer-facing actions.
- Keep morale and attendance indicators aggregate-only unless a compliant employee-level model is explicitly approved later.

## ForgeQC audit position

ForgeQC should be treated as the source candidate for specialized quality workflows. Expected reusable areas include:

- RMA tracking
- NCR, DMR, CAPA, and deviation workflow
- customer, part, and work-order quality history
- reason-code and defect trend reporting
- containment, root cause, corrective action, owner, due-date, and closure lifecycle
- quality metrics feeding reporting and Company Pulse
- quote/BOM quality review logic, if present

Before moving code, inspect actual ForgeQC files and map its models/routes to MFGForge tables. If ForgeQC contains private data, real customers, real RMA records, or local databases, do not commit them.

## ForgeVault audit position

ForgeVault should be treated as the source candidate for controlled vendor, purchased part, material, supplier, document, and traceability logic. Expected reusable areas include:

- vendor part intake
- supplier records
- approved purchased part records
- controlled material records
- document metadata and revision handling
- McMaster-style vendor data intake patterns
- material cert and traceability-adjacent workflows

Before moving code, inspect actual ForgeVault files and map reusable logic into MFGForge vault and material modules. Do not commit proprietary documents, customer drawings, quote PDFs, vendor exports, private cert files, or local storage paths.

## PM Tracking audit position

PM Tracking is pending local file audit.

Known details to preserve:

- Path: `C:\Users\dboone\PM Tracking`
- Launch command: `python -c "exec(open('main.txt', encoding='utf-8').read())"`
- Stack: Flask + openpyxl + sqlite3
- Known files: `pm_data.xlsx`, `pm_app.db`
- Known features: dark dashboard UI, machine status cards, machine detail pages, manual operator completion entry, QR Codes page with printable SVG QR labels, and Excel export at `/export.xlsx`

Expected reusable areas include:

- machine readiness and PM status cards
- machine detail workflow
- PM schedule and completion history
- manual completion entry
- QR label generation and routing
- Excel export patterns
- maintenance ticket form, if implemented later

Do not commit `pm_data.xlsx`, `pm_app.db`, machine history, employee-level completion data, or private shop records.

## SuperForge_Unofficial audit position

`SuperForge_Unofficial` should not become the application source of truth. Its proper role is:

- compiled libraries
- Windows executable release candidates
- installer experiments
- generated manifests
- checksums
- sanitized build logs
- packaging notes

The source repo remains MFGForge. Build artifacts should trace back to a specific MFGForge commit.
