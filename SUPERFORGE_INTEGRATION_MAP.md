# SuperForge Integration Map

Date: 2026-05-14
Target repo: `danieloculus0-bot/MFGForge`
Repair note: this document is intentionally documentation-only. It does not change runtime code, schema, tests, packaging scripts, or build artifacts.

## Primary decision

MFGForge remains the source-of-truth app repo for the SuperForge ERP Suite.

`SuperForge_Unofficial` is only the build artifact and unofficial distribution repo. It may receive compiled libraries, release candidates, manifests, checksums, packaging notes, and installer experiments, but it should not receive live application source code as the canonical implementation.

PM Tracking is a behavioral reference only. PM will be rebuilt natively inside MFGForge/SuperForge as `modules/pm` instead of copied from the old app.

## Target module architecture

```text
mfgforge/
  core/
    app_factory.py
    database.py
    module_registry.py
    navigation.py
    audit.py
    permissions.py
  modules/
    qc/
      routes.py
      services.py
      reports.py
      models.sql
      templates/
    vault/
      routes.py
      services.py
      storage.py
      models.sql
      templates/
    pm/
      routes.py
      services.py
      qr.py
      exports.py
      models.sql
      templates/
    quoting/
      routes.py
      bom_extract.py
      material_assignment.py
      models.sql
      templates/
    planning/
      routes.py
      watchlists.py
      capacity.py
      models.sql
      templates/
    intelligence/
      routes.py
      recommendations.py
      approval_workflows.py
      models.sql
      templates/
    reporting/
      routes.py
      metrics.py
      exports.py
      models.sql
      templates/
  templates/
    base.html
    dashboard.html
  static/
    app.css
```

This is a target layout, not an immediate refactor order. The current app should stay working while modules are extracted one piece at a time.

## What moves from ForgeQC

Move only verified, reusable logic after inspecting actual ForgeQC files.

Candidate logic for `modules/qc` includes RMA, NCR, DMR, CAPA, deviation request workflow, quality event lifecycle fields, customer/part/work-order quality history, reason-code and defect trend logic, quality metrics and Pareto/reporting logic, FAIR or inspection report helpers if present, and quote/BOM quality review logic if present.

Expected MFGForge anchor tables include `quality_events`, `deviations`, `reason_codes`, `customers`, `parts`, `work_orders`, `fpy_summaries`, `dashboard_metric_snapshots`, and `ai_action_log`.

Do not move real RMA data, real customer records, defect logs, inspection results, private Excel trackers, local databases, or customer-facing artifacts.

## What moves from ForgeVault

Move only verified, reusable logic after inspecting actual ForgeVault files.

Candidate logic for `modules/vault` includes vendor part intake, supplier and purchased part records, approved material records, McMaster-style vendor data intake patterns, controlled document metadata, document revision and approval status, material cert traceability helpers, document-to-ERP-record link patterns, search and retrieval patterns, and storage abstraction logic that avoids committing private files.

Expected MFGForge anchor tables include `suppliers`, `materials`, `material_certificates`, `documents`, `parts`, `quote_intakes`, and `work_orders`.

Do not move proprietary customer drawings, quote PDFs, cert files, vendor exports, runtime databases, local storage folders, or private document examples.

## Native PM rebuild

PM Tracking does not move as source code. It is a behavioral reference only.

Known reference behavior:

- machine status card logic
- machine detail page workflow
- manual operator completion entry
- QR code label generation and printable label workflow
- PM completion history
- PM schedule and overdue logic
- Excel export workflow
- maintenance ticket form if implemented
- dark dashboard UI patterns that fit the SuperForge interface

Native MFGForge/SuperForge rebuild targets for `modules/pm`:

- machine assets and PM assets
- machine readiness status
- PM schedules
- PM completion history
- maintenance tickets
- secure QR label workflow
- Excel import/export adapters
- planning risk signals
- Company Pulse maintenance signals

Expected MFGForge anchor tables:

- `pm_assets`
- `machine_assets`
- future `pm_schedules`
- future `pm_completion_history`
- future `pm_tickets`
- future `pm_asset_status_snapshots`
- `departments`
- `dashboard_metric_snapshots`

Do not move `pm_data.xlsx`, `pm_app.db`, employee-level data, machine-history private records, exported spreadsheets, or QR links that expose local paths or unauthenticated mutable actions.

## What stays native in MFGForge

The following should remain native MFGForge concepts:

- application factory and local Flask runtime
- SQLite schema and future migrations
- ERP master data
- customers, suppliers, departments, reason codes, operating profiles
- parts and work orders
- material catalog and material certificate control
- quote intake, PDF BOM candidates, BOM reviews, and quote material drafts
- planning and purchasing watchlists
- native PM rebuild and machine-readiness signals
- Company Pulse and dashboard metric snapshots
- AI governance through `ai_action_log`
- privacy-safe aggregate morale indicators
- Windows executable build source and packaging scripts

## Overlap map

| Concept | MFGForge anchor | Expected source/reference overlap | Decision |
| --- | --- | --- | --- |
| Customers | `customers` | ForgeQC customer quality history | MFGForge owns identity. Source modules attach history. |
| Suppliers | `suppliers` | ForgeVault supplier/vendor records | MFGForge owns supplier identity. ForgeVault contributes intake/detail logic. |
| Materials | `materials` | ForgeVault approved material and vendor part logic | MFGForge owns material identity. ForgeVault contributes enrichment and traceability. |
| Material certs | `material_certificates` | ForgeVault cert/reference logic | MFGForge owns cert records. Vault contributes document control and storage references. |
| Parts | `parts` | ForgeQC part quality history, ForgeVault part docs | MFGForge owns part identity. |
| Work orders | `work_orders` | ForgeQC quality events, PM downtime context | MFGForge owns work-order identity. |
| Quality events | `quality_events` | ForgeQC RMA/NCR/DMR/CAPA | Use ForgeQC lifecycle logic only after mapping to MFGForge identity. |
| Deviations | `deviations` | ForgeQC deviation workflow | Preserve MFGForge approval control. Add stronger workflow fields only after audit. |
| Documents | `documents` | ForgeVault document vault | Use ForgeVault workflow, but MFGForge owns ERP links. |
| PM assets | `pm_assets`, `machine_assets` | PM Tracking machine cards and detail behavior | Rebuild natively in MFGForge. Do not copy old PM app source. |
| QR labels | future `modules/pm/qr.py` | PM Tracking QR page behavior | Rebuild securely and route-safe. |
| Quoting | `quote_intakes`, `pdf_bom_candidates`, `bom_reviews`, `quote_material_drafts` | ForgeQC quote review, ForgeVault drawing refs | MFGForge owns quoting flow. External logic feeds review and references. |
| Planning | `planning_watchlists`, `purchasing_watchlists` | PM downtime, supplier risk, quality risk | MFGForge owns planning signals. |
| Intelligence | `ai_action_log`, future `modules/intelligence` | All modules | MFGForge governs AI assistance and approval logging. |
| Reporting | `dashboard_metric_snapshots`, future `modules/reporting` | Quality, PM, supplier, planning signals | MFGForge aggregates reporting. |

## Best source by final module

| Final module | Best source | Reason |
| --- | --- | --- |
| `core` | MFGForge | Active app host, schema owner, navigation, governance, local runtime. |
| `modules/qc` | ForgeQC plus MFGForge anchors | ForgeQC should contribute specialized QC workflows after audit. MFGForge keeps ERP identity. |
| `modules/vault` | ForgeVault plus MFGForge anchors | ForgeVault should contribute vendor/document patterns after audit. MFGForge keeps links and source of truth. |
| `modules/pm` | Native MFGForge rebuild using PM Tracking behavior as reference | Avoid copying legacy app guts while preserving proven workflow behavior. |
| `modules/quoting` | MFGForge | Current quote intake, BOM candidate, review, and material draft flow are native. |
| `modules/planning` | MFGForge | Watchlists and capacity-risk logic belong in the ERP host. |
| `modules/intelligence` | MFGForge | AI must be centralized, approval-gated, and logged. |
| `modules/reporting` | MFGForge | Reporting needs cross-module ERP data. |

## Safest migration sequence

1. Keep the current MFGForge baseline working.
2. Merge documentation-only audit and map work first.
3. Treat PM Tracking as behavioral reference only and rebuild PM natively inside MFGForge.
4. Audit ForgeQC files directly and update this map with exact routes, models, schemas, tests, and utilities.
5. Audit ForgeVault files directly and update this map with exact routes, models, schemas, tests, and utilities.
6. Add tests around current MFGForge app behavior before major refactoring.
7. Reconcile `app.py` registry logic with `module_registry.py` so there is one source of truth.
8. Create empty `core` and `modules/*` folders only after tests protect current behavior.
9. Move MFGForge-native code into `core`, `modules/quoting`, `modules/planning`, `modules/intelligence`, and `modules/reporting` first.
10. Add the native PM skeleton, schema draft, read-only dashboard route, and tests before QR write actions.
11. Add ForgeVault document and supplier/material logic through empty migrations and import adapters, not data copy.
12. Add ForgeQC quality workflow logic through mapped services and controlled extension tables, not duplicate disconnected tables.
13. Wire reporting after core workflows exist.
14. Wire intelligence last so recommendations remain read-only or approval-gated.
15. Build Windows executable from MFGForge source, then copy intentional artifacts into `SuperForge_Unofficial` release-candidate folders.

## Human-in-the-loop AI rule

AI can assist like GPS. It may summarize, draft, flag risk, suggest actions, and prepare review packets.

AI must not silently approve or execute BOM approval, material assignment approval, material cert approval, deviation approval, quality event closure, quote release, shipment readiness, purchasing action, PM closure, machine readiness release, customer-facing communication, or employee-level morale or performance decisions.

Every business-critical AI suggestion must have human approval status and audit traceability.