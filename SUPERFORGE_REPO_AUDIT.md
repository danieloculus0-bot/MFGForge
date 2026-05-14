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
