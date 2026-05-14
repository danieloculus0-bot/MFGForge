# SuperForge Repository Audit for MFGForge Integration

Date: 2026-05-14
Target repo: `danieloculus0-bot/MFGForge`
Target branch: `integration/superforge-suite`

## Scope and access status

This audit is limited to repository/system files available from the MFGForge working copy and the explicitly known PM Tracking details supplied for this task.

| Source | Access status | Notes |
| --- | --- | --- |
| `danieloculus0-bot/MFGForge` | Audited locally | Active ERP target in `/workspace/MFGForge`. |
| `danieloculus0-bot/ForgeQC` | Pending source access | Not present in this workspace. Direct `git ls-remote` over HTTPS was blocked by the environment with `CONNECT tunnel failed, response 403`, so no file-level claims are made here. |
| `danieloculus0-bot/ForgeVault` | Pending source access | Not present in this workspace. Direct `git ls-remote` over HTTPS was blocked by the environment with `CONNECT tunnel failed, response 403`, so no file-level claims are made here. |
| PM Tracking | Pending local audit | Local Windows path is known, but files are not present in this Linux workspace. Only user-provided known details are included. |

## MFGForge

### Repo/system purpose and role

MFGForge is the active manufacturing ERP foundation for small and mid-size fabrication and contract manufacturing shops. It is the integration target for the SuperForge suite and should remain the system of record for ERP master data, production records, quality records, preventive-maintenance records, planning records, quoting records, reporting snapshots, morale/strain indicators, and AI governance logs.

### App entrypoints

- `app.py`: Flask application factory, database initialization, generic module registry, generic list/new-record routes, dashboard, and AI policy route.
- `smoke_test.py`: executable smoke test entrypoint for app creation, page access, generic module route checks, and persistence checks.
- `flask --app app run`: documented local run command.

### Schemas/database files

- `schema.sql`: durable SQLite schema.
- Tables currently present:
  - `system_meta`
  - `customers`
  - `suppliers`
  - `departments`
  - `reason_codes`
  - `operating_profiles`
  - `parts`
  - `work_orders`
  - `quality_events`
  - `deviations`
  - `documents`
  - `pm_assets`
  - `morale_snapshots`
  - `materials`
  - `quote_intakes`
  - `pdf_bom_candidates`
  - `bom_reviews`
  - `quote_material_drafts`
  - `planning_watchlists`
  - `purchasing_watchlists`
  - `fpy_summaries`
  - `operator_efficiency_baselines`
  - `quoting_throughput_baselines`
  - `dashboard_metric_snapshots`
  - `ai_action_log`
- No local committed SQLite database should be treated as source data.

### Route files

MFGForge currently uses one route file:

- `app.py`
  - `/`: ERP dashboard.
  - `/ai-policy`: human-in-the-loop AI policy screen.
  - `/records/<module_key>`: generic module list route.
  - `/records/<module_key>/new`: generic module record creation route.

### Utility modules

- `module_registry.py`: older standalone module registry and `field()` helper. It overlaps conceptually with the current in-file `MODULES` list in `app.py` and should not become a second independent source of truth without reconciliation.
- `app.py`: includes small data-layer helpers such as database access, initialization, table counts, record insertion, and select-option loading.

### Templates/static assets

- MFGForge currently uses inline Jinja templates through `render_template_string` in `app.py`.
- No separate `templates/` directory is present in the current working copy.
- No separate `static/` directory is present in the current working copy.

### Tests

- `smoke_test.py` creates a temporary SQLite database, initializes the Flask app in testing mode, verifies dashboard and policy pages, verifies every registered module list/new route, posts representative records through the generic form route, and validates selected persisted foreign keys/status values.
- There is no separate unit-test package in the current working copy.

### Packaging/runtime files

- `requirements.txt`: Flask dependency.
- `README.md`: project purpose, included modules, local run command, smoke-test command, GitHub Actions note, and data-privacy rules.
- `AGENTS.md`: repository-specific agent instructions, product purpose, workflow rules, privacy rules, AI human-in-the-loop rules, and development standard.
- `MFGFORGE_MODULE_BLUEPRINT.md`: active functional scope and implementation rules.

### Reusable logic found

- Generic module declaration pattern with fields, select sources, labels, and module metadata.
- Generic CRUD-lite routing for list and create flows.
- Durable SQLite schema covering the first ERP foundation layer.
- Privacy-safe aggregate morale schema and AI action-log schema.
- Quoting foundation tables for quote intake, PDF BOM candidates, BOM review, and material assignment drafts.
- Planning and purchasing watchlist tables.
- FPY, operator-efficiency, quoting-throughput, and dashboard metric snapshot tables.

### Duplicate or overlapping logic

- `app.py` and `module_registry.py` both define a `field()` helper and module metadata concepts. The active app uses `app.py`; `module_registry.py` should be reconciled or retired before modularization.
- `quality_events` covers broad event types including RMA/NCR/DMR/CAPA/customer complaints, while dedicated future QC modules from ForgeQC may have more specific workflows. The integration must avoid creating disconnected duplicate quality tables.
- `documents` provides document-control references, while ForgeVault is expected to contribute vault/document logic. Integration should map ForgeVault concepts into MFGForge document control rather than create a parallel document store.
- `pm_assets` provides a preventive-maintenance asset foundation, while PM Tracking is expected to include machine cards, machine detail pages, completions, QR labels, Excel export, and local files/databases. The integration should avoid splitting asset identity between two systems.

### Known risks or conflicts

- MFGForge is currently monolithic in `app.py`; direct code moves from ForgeQC, ForgeVault, or PM Tracking should wait until target package folders exist.
- Existing module metadata duplication may cause drift if both `app.py` and `module_registry.py` are updated independently.
- SQLite table names and source-system table names may differ. Migration should start with mapping and import adapters, not blind table replacement.
- PM Tracking references `pm_data.xlsx` and `pm_app.db`, which may contain private operational records. Those files must not be committed to MFGForge.
- Any quality, document, or PM automation must preserve human approval for record closing, deviation approval, inventory impact, external communication, and business-critical execution.
- Morale and attendance-related data must remain aggregate-only unless a compliant model is explicitly approved.

## ForgeQC

### Repo/system purpose and role

ForgeQC is expected to be the source candidate for quality-management workflows that can strengthen MFGForge's native quality foundation. Based on MFGForge's target scope, candidate areas include RMA tracking, NCR/DMR/CAPA workflows, deviation handling, FAIR/inspection support, quality metrics, reason-code trends, containment/root-cause/corrective-action workflow, and customer/part/work-order quality history.

### App entrypoints

- Pending source access. No ForgeQC files are present in the workspace, and remote source access was blocked.

### Schemas/database files

- Pending source access. Do not invent ForgeQC schemas until the repository is available for audit.

### Route files

- Pending source access. Do not invent ForgeQC routes until the repository is available for audit.

### Utility modules

- Pending source access.

### Templates/static assets

- Pending source access.

### Tests

- Pending source access.

### Packaging/runtime files

- Pending source access.

### Reusable logic found

- Pending source access. Expected candidate logic should be verified before migration: quality record lifecycle, report generation, trend summaries, inspection/FAIR helpers, CAPA drafting support, and audit/history handling.

### Duplicate or overlapping logic

- Expected overlap with MFGForge `quality_events`, `deviations`, `reason_codes`, `fpy_summaries`, `dashboard_metric_snapshots`, and `ai_action_log`.

### Known risks or conflicts

- Risk of duplicating quality event identity if ForgeQC has separate RMA/NCR/DMR/CAPA tables that are imported without mapping.
- Risk of losing auditability if ForgeQC workflow state changes are copied as direct edits without MFGForge audit/action logging.
- Risk of fake/demo or private quality data being copied. Only schema, reusable code, empty migrations, and approved synthetic tests should move.

## ForgeVault

### Repo/system purpose and role

ForgeVault is expected to be the source candidate for document vault, file/reference, revision, approval, access, and retrieval logic that can strengthen MFGForge's native `documents` table and future `modules/vault` package.

### App entrypoints

- Pending source access. No ForgeVault repository files are present in the workspace, and remote source access was blocked.

### Schemas/database files

- Pending source access. Do not invent ForgeVault schemas until the repository is available for audit.

### Route files

- Pending source access. Do not invent ForgeVault routes until the repository is available for audit.

### Utility modules

- Pending source access.

### Templates/static assets

- Pending source access.

### Tests

- Pending source access.

### Packaging/runtime files

- Pending source access.

### Reusable logic found

- Pending source access. Expected candidate logic should be verified before migration: document metadata, revision controls, storage references, search/filtering, approval status, access rules, and document-to-ERP-record linking.

### Duplicate or overlapping logic

- Expected overlap with MFGForge `documents`, `quote_intakes.drawing_reference`, `pdf_bom_candidates.candidate_source`, and potential future attachment links for quality/work-order/part records.

### Known risks or conflicts

- Risk of committing proprietary drawings, quote PDFs, exports, or customer documents. Integration must use references/import paths and empty schema, not real files.
- Risk of conflicting document status/revision semantics between ForgeVault and MFGForge.
- Risk of local-file assumptions that do not work in deployed ERP environments.

## PM Tracking

### Repo/system purpose and role

PM Tracking is a preventive-maintenance system candidate for migration into MFGForge's future `modules/pm` package. It should contribute machine-centric PM workflow ideas while MFGForge remains the ERP system of record.

### Known access details
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

### Known features

- Machine status cards.
- Machine detail pages.
- Manual completion entry.
- QR labels.
- Excel export.
- `pm_data.xlsx`.
- `pm_app.db`.

### App entrypoints

- Known launch entrypoint is `main.txt` executed through Python.
- Full file-level audit is pending local access to `C:\Users\dboone\PM Tracking`.

### Schemas/database files

- Known database/file artifacts: `pm_app.db` and `pm_data.xlsx`.
- Full schema audit is pending local access.
- These artifacts may contain real shop data and must not be committed to MFGForge.

### Route files

- Pending local audit.

### Utility modules

- Pending local audit.

### Templates/static assets

- Pending local audit.

### Tests

- Pending local audit.

### Packaging/runtime files

- Pending local audit.

### Reusable logic found

- Machine/asset status-card presentation.
- Machine detail workflow.
- Manual PM completion flow.
- QR label generation/printing flow.
- Excel export flow.
- SQLite-backed PM storage pattern.

### Duplicate or overlapping logic

- Expected overlap with MFGForge `pm_assets`, `departments`, `dashboard_metric_snapshots`, and future PM completion/history tables.

### Known risks or conflicts

- `pm_data.xlsx` and `pm_app.db` are likely runtime/data artifacts and should remain out of Git unless explicitly converted into empty schema/migration/test fixtures.
- PM Tracking may identify individual operators or technicians. MFGForge should avoid employee-level private identifiers unless an approved compliant model exists.
- QR label URLs/identifiers may assume local paths or ports; they need a deployed ERP-safe routing model before migration.
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
