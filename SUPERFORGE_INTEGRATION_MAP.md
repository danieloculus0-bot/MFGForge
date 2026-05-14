# SuperForge Integration Map for MFGForge

Date: 2026-05-14
Target repo: `danieloculus0-bot/MFGForge`
Target branch: `integration/superforge-suite`

## Integration principle

MFGForge remains the active ERP host. ForgeQC, ForgeVault, and PM Tracking should be treated as source systems for reusable workflow logic, schemas, UI patterns, and migration adapters. Do not import private runtime data, proprietary drawings, local databases, Excel trackers, customer names, defect logs, or fake demo records.

## Target architecture

```text
mfgforge/
  core/
    app_factory.py
    database.py
    module_registry.py
    authz.py
    audit.py
    navigation.py
  modules/
    qc/
      routes.py
      models.sql
      services.py
      reports.py
      templates/
    vault/
      routes.py
      models.sql
      services.py
      storage.py
      templates/
    pm/
      routes.py
      models.sql
      services.py
      qr.py
      exports.py
      templates/
    quoting/
      routes.py
      models.sql
      bom_extract.py
      material_assignment.py
      templates/
    planning/
      routes.py
      models.sql
      watchlists.py
      templates/
    intelligence/
      routes.py
      models.sql
      recommendations.py
      approval_workflows.py
      templates/
    reporting/
      routes.py
      models.sql
      metrics.py
      exports.py
      templates/
  templates/
    base.html
    dashboard.html
  static/
    app.css
```

This is a proposed layout only. Runtime refactoring should happen in later incremental commits, after the two source-repo audits are complete and after MFGForge's current monolithic `app.py` routes are protected by tests.

## What logic moves from ForgeQC

ForgeQC source files were not available in this workspace, so this section lists integration targets that must be verified against the actual ForgeQC repository before code migration.

Move verified ForgeQC logic into `modules/qc` when available:

- RMA workflow logic that improves or specializes MFGForge's current broad `quality_events` model.
- NCR, DMR, CAPA, customer-complaint, and inspection-reject workflows.
- Containment, root-cause, corrective-action, owner, due-date, and closure workflows.
- FAIR/inspection report generation if present and reusable.
- Quality trend and metric calculations that can feed `dashboard_metric_snapshots` and `reporting`.
- Reason-code categorization or defect taxonomy, if stronger than MFGForge's current `reason_codes` table.
- Human-in-the-loop AI drafting helpers for quality language, if present, routed through `modules/intelligence` and `ai_action_log` rather than direct auto-closure.

Do not move without review:

- Real quality records, customer names, defect logs, RMA examples, inspection results, or attachments.
- Any logic that closes quality records, approves deviations, or notifies customers without explicit human approval and audit logging.

## What logic moves from ForgeVault

ForgeVault source files were not available in this workspace, so this section lists integration targets that must be verified against the actual ForgeVault repository before code migration.

Move verified ForgeVault logic into `modules/vault` when available:

- Document metadata, revision, status, owner, and storage-reference handling.
- File reference and retrieval workflows that can extend MFGForge's `documents` table.
- Document-to-ERP linking for parts, work orders, quality events, deviations, quote intakes, and PM assets.
- Search/filter UI patterns for document lookup.
- Approval/release workflow patterns for controlled documents.
- Storage abstraction logic if it avoids committing customer documents or drawings.

Do not move without review:

- Proprietary drawings, quote PDFs, customer document examples, exports, private files, or local absolute storage paths.
- Any document release/approval automation that bypasses human approval.

## What logic moves from PM Tracking

PM Tracking files are unavailable in this workspace and are pending local audit at `C:\Users\dboone\PM Tracking`. Only the known details supplied for this task are mapped here.

Move verified PM Tracking logic into `modules/pm` after local audit:

- Machine status card logic.
- Machine detail page workflow.
- Manual completion entry workflow.
- QR label generation/routing logic.
- Excel export logic, implemented as an export from approved MFGForge records rather than as the system of record.
- SQLite schema concepts from `pm_app.db`, translated into MFGForge schema migrations after private data is excluded.
- Relevant import logic from `pm_data.xlsx`, implemented as an explicit import path that Daniel can run locally against private files.

Known PM Tracking details to preserve during audit:

- Path: `C:\Users\dboone\PM Tracking`
- Launch command: `python -c "exec(open('main.txt', encoding='utf-8').read())"`
- Stack: Flask + openpyxl + sqlite3
- Features: machine status cards, machine detail pages, manual completion entry, QR labels, Excel export, `pm_data.xlsx`, `pm_app.db`

Do not move without review:

- `pm_data.xlsx` or `pm_app.db` contents.
- Private machine history or employee-level completion data.
- QR labels that expose private local paths or unauthenticated mutable actions.

## What stays native in MFGForge

The following foundations should remain native MFGForge concepts and should be extended rather than replaced:

- ERP master data: `customers`, `suppliers`, `departments`, `reason_codes`, `parts`, `materials`, and `operating_profiles`.
- Production foundation: `work_orders` and part/customer linkage.
- Quality foundation: `quality_events`, `deviations`, `fpy_summaries`, and reason-code relationships.
- Document-control foundation: `documents` and references from quote/customer/quality/part/work-order records.
- PM foundation: `pm_assets` and future PM completion/history tables.
- Quoting foundation: `quote_intakes`, `pdf_bom_candidates`, `bom_reviews`, and `quote_material_drafts`.
- Planning/purchasing foundation: `planning_watchlists` and `purchasing_watchlists`.
- Performance/reporting foundation: `operator_efficiency_baselines`, `quoting_throughput_baselines`, and `dashboard_metric_snapshots`.
- AI governance: `ai_action_log`, human approval state, and audit-first assistant behavior.
- Privacy-safe morale/strain indicators: `morale_snapshots` by aggregate period/department.

## Overlapping tables/concepts

| Concept | MFGForge native table/concept | Expected ForgeQC overlap | Expected ForgeVault overlap | Expected PM Tracking overlap | Integration decision |
| --- | --- | --- | --- | --- | --- |
| Customers | `customers` | Customer-linked quality history | Customer document links | None expected | MFGForge remains source of truth. |
| Suppliers/materials | `suppliers`, `materials` | Supplier quality may overlap | Supplier cert/document links | None expected | MFGForge remains source of truth; external modules attach references. |
| Parts | `parts` | Part quality history, FAIR | Drawings/spec documents | PM spare references may appear | MFGForge remains source of truth. |
| Work orders | `work_orders` | Work-order quality events | Work-order docs | Possible maintenance downtime context | MFGForge remains source of truth. |
| Quality events | `quality_events` | RMA/NCR/DMR/CAPA workflows | Quality attachments | None expected | Use ForgeQC workflow if verified stronger; store in MFGForge schema or mapped extension tables. |
| Deviations | `deviations` | Deviation approval workflow | Deviation docs | None expected | Preserve MFGForge approval status; add ForgeQC workflow fields only after audit. |
| Documents | `documents` | Quality attachments | Vault metadata/revision/search | PM manuals/QR attachments | Use ForgeVault as best source for document workflow, mapped to MFGForge document identity. |
| PM assets | `pm_assets` | None expected | PM manuals/docs | Machine cards/details/completions | Use PM Tracking as best source for PM workflow, mapped to MFGForge asset identity. |
| PM completions | Future PM history table | None expected | PM completion attachments | Manual completion entry | PM Tracking likely best source after audit. |
| QR labels | Future PM route/label support | None expected | Document QR links may exist | QR labels | PM Tracking likely best source after audit; harden routes before use. |
| Quote intake | `quote_intakes` | Quality history context | Drawing references | None expected | MFGForge native. |
| BOM extraction/review | `pdf_bom_candidates`, `bom_reviews` | Inspection/FAIR context may overlap | Drawing source files | None expected | MFGForge native with vault document references. |
| AI assistance | `ai_action_log` | Quality drafts/trends | Document summaries | PM recommendations | MFGForge intelligence module is governance layer; source modules provide read-only signals/drafts. |
| Reporting | `dashboard_metric_snapshots` | Quality metrics | Document metrics | PM compliance metrics | MFGForge reporting module aggregates across modules. |

## Best source implementation by module

| Final module | Best source | Rationale |
| --- | --- | --- |
| `core` | MFGForge | Active app, schema initialization, ERP identity, navigation, privacy rules, and AI governance expectations already live here. |
| `modules/qc` | ForgeQC after source audit; MFGForge for base tables | ForgeQC should provide specialized quality workflow if verified; MFGForge already has broad quality tables and ERP links. |
| `modules/vault` | ForgeVault after source audit; MFGForge for document identity | ForgeVault should provide document workflow if verified; MFGForge should retain ERP references and avoid private file commits. |
| `modules/pm` | PM Tracking after local audit; MFGForge for asset identity | PM Tracking known features match PM workflow; MFGForge already has `pm_assets` and department linkage. |
| `modules/quoting` | MFGForge | Current native schema covers quote intake, PDF BOM candidates, BOM review, and quote material drafts. |
| `modules/planning` | MFGForge | Current native schema covers planning and purchasing watchlists tied to ERP records. |
| `modules/intelligence` | MFGForge | Human-in-the-loop governance must be central and logged in `ai_action_log`. Source modules may provide prompts/signals only. |
| `modules/reporting` | MFGForge | Dashboard snapshots and aggregate operational metrics should be cross-module and ERP-native. |

## Safest migration sequence

1. **Freeze the current MFGForge baseline.** Keep the current smoke test passing before any modular refactor.
2. **Complete source access audits.** Audit ForgeQC and ForgeVault from actual repository files; audit PM Tracking locally at `C:\Users\dboone\PM Tracking` without committing private data.
3. **Create empty target package folders.** Add `core` and `modules/*` folders with no runtime behavior changes, if a later task approves refactoring.
4. **Extract MFGForge module registry first.** Reconcile the duplicate `MODULES`/`field()` concepts in `app.py` and `module_registry.py` into one source of truth.
5. **Move native MFGForge schemas into grouped migrations.** Keep existing table names stable and add tests before adding external module tables.
6. **Integrate ForgeVault document metadata.** Map document/revision/storage-reference concepts to `documents`; add document links before importing any file handling.
7. **Integrate ForgeQC workflows.** Map RMA/NCR/DMR/CAPA/deviation workflows onto `quality_events` and `deviations`, adding extension tables only where the audited source has necessary lifecycle detail.
8. **Integrate PM Tracking workflow.** Add PM completion/history tables, machine detail views, QR routes, and Excel export from MFGForge records. Keep `pm_data.xlsx` and `pm_app.db` local-only.
9. **Connect quoting to vault.** Reference customer drawings through `documents`/vault storage references while preserving human BOM review before quote use.
10. **Connect reporting.** Feed quality, PM, quoting, planning, purchasing, and morale summaries into `dashboard_metric_snapshots` or reporting service queries.
11. **Connect intelligence last.** Add read-only recommendations/drafts after workflows exist; require explicit approval, execution logging, and audit trails for all business-critical actions.
12. **Retire transitional duplicates.** Remove obsolete duplicate registries/routes only after smoke tests and module-specific tests cover the replacement paths.

## Non-negotiable controls

- Do not commit private files, runtime databases, Excel trackers, customer documents, or proprietary drawings.
- Do not create fake business data to prove integration.
- Do not allow AI to close records, approve deviations, change inventory, release jobs, send external emails, or make personnel decisions without human approval and audit logging.
- Keep morale/attendance indicators aggregate-only unless Daniel explicitly approves a compliant employee-level data model.
- Prefer import adapters and empty schemas over direct data copy.
