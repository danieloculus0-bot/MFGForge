# SuperForge Integration Map

Date: 2026-05-14
Target repo: `danieloculus0-bot/MFGForge`
Repair note: this document is intentionally documentation-only. It does not change runtime code, schema, tests, packaging scripts, or build artifacts.

## Primary decision

MFGForge remains the source-of-truth app repo for the SuperForge ERP Suite.

`SuperForge_Unofficial` is only the build artifact and unofficial distribution repo. It may receive compiled libraries, release candidates, manifests, checksums, packaging notes, and installer experiments, but it should not receive live application source code as the canonical implementation.

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

Candidate logic for `modules/qc`:

- RMA workflow
- NCR workflow
- DMR workflow
- CAPA workflow
- deviation request workflow if stronger than MFGForge's native version
- quality event lifecycle fields such as containment, root cause, corrective action, owner, due date, review status, and closure status
- customer, part, and work-order quality history
- reason-code and defect trend logic
- quality metrics and Pareto/reporting logic
- FAIR or inspection report helpers, if present
- quote/BOM quality review logic, if present

Expected MFGForge anchor tables:

- `quality_events`
- `deviations`
- `reason_codes`
- `customers`
- `parts`
- `work_orders`
- `fpy_summaries`
- `dashboard_metric_snapshots`
- `ai_action_log`

Do not move real RMA data, real customer records, defect logs, inspection results, private Excel trackers, local databases, or customer-facing artifacts.

## What moves from ForgeVault

Move only verified, reusable logic after inspecting actual ForgeVault files.

Candidate logic for `modules/vault`:

- vendor part intake
- supplier and purchased part records
- approved material records
- McMaster-style vendor data intake patterns
- controlled document metadata
- document revision and approval status
- material cert traceability helpers
- document-to-ERP-record link patterns
- search and retrieval patterns
- storage abstraction logic that avoids committing private files

Expected MFGForge anchor tables:

- `suppliers`
- `materials`
- `material_certificates`
- `documents`
- `parts`
- `quote_intakes`
- `work_orders`

Do not move proprietary customer drawings, quote PDFs, cert files, vendor exports, runtime databases, local storage folders, or private document examples.

## What moves from PM Tracking

PM Tracking is pending local audit. Move only verified logic from `C:\Users\dboone\PM Tracking` after inspecting `main.txt`, `pm_data.xlsx`, `pm_app.db`, route logic, templates, QR generation, and export behavior.

Known candidate logic for `modules/pm`:

- machine status card logic
- machine detail page workflow
- manual operator completion entry
- QR code label generation and printable label workflow
- PM completion history
- PM schedule and overdue logic
- Excel export workflow
- maintenance ticket form if implemented
- dark dashboard UI patterns that fit the SuperForge interface

Expected MFGForge anchor tables:

- `pm_assets`
- `machine_assets`
- future PM schedule table
- future PM completion history table
- future maintenance ticket table
- `departments`
- `dashboard_metric_snapshots`

Do not move `pm_data.xlsx`, `pm_app.db`, employee-level data, machine-history private records, or QR links that expose local paths or unauthenticated mutable actions.

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
- Company Pulse and dashboard metric snapshots
- AI governance through `ai_action_log`
- privacy-safe aggregate morale indicators
- Windows executable build source and packaging scripts

## Overlap map

| Concept | MFGForge anchor | Expected source overlap | Decision |
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
| PM assets | `pm_assets`, `machine_assets` | PM Tracking machine cards and detail pages | Use PM Tracking workflow, MFGForge owns asset identity. |
| QR labels | future `modules/pm/qr.py` | PM Tracking QR page | Preserve if secure and route-safe. |
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
| `modules/pm` | PM Tracking plus MFGForge anchors | PM Tracking has the working machine/PM workflow. MFGForge keeps asset identity and ERP integration. |
| `modules/quoting` | MFGForge | Current quote intake, BOM candidate, review, and material draft flow are native. |
| `modules/planning` | MFGForge | Watchlists and capacity-risk logic belong in the ERP host. |
| `modules/intelligence` | MFGForge | AI must be centralized, approval-gated, and logged. |
| `modules/reporting` | MFGForge | Reporting needs cross-module ERP data. |

## Safest migration sequence

1. Keep the current MFGForge baseline working.
2. Merge documentation-only audit and map work first.
3. Audit ForgeQC files directly and update this map with exact routes, models, schemas, tests, and utilities.
4. Audit ForgeVault files directly and update this map with exact routes, models, schemas, tests, and utilities.
5. Audit PM Tracking locally at `C:\Users\dboone\PM Tracking` without committing private files.
6. Add tests around current MFGForge app behavior before major refactoring.
7. Reconcile `app.py` registry logic with `module_registry.py` so there is one source of truth.
8. Create empty `core` and `modules/*` folders only after tests protect current behavior.
9. Move MFGForge-native code into `core`, `modules/quoting`, `modules/planning`, `modules/intelligence`, and `modules/reporting` first.
10. Add ForgeVault document and supplier/material logic through empty migrations and import adapters, not data copy.
11. Add ForgeQC quality workflow logic through mapped services and controlled extension tables, not duplicate disconnected tables.
12. Add PM Tracking PM workflow through mapped services, QR routes, and export logic after local audit.
13. Wire reporting after core workflows exist.
14. Wire intelligence last so recommendations remain read-only or approval-gated.
15. Build Windows executable from MFGForge source, then copy intentional artifacts into `SuperForge_Unofficial` release-candidate folders.

## Human-in-the-loop AI rule

AI can assist like GPS. It may summarize, draft, flag risk, suggest actions, and prepare review packets.

AI must not silently approve or execute:

- BOM approval
- material assignment approval
- material cert approval
- deviation approval
- quality event closure
- quote release
- shipment readiness
- purchasing action
- PM closure
- machine readiness release
- customer-facing communication
- employee-level morale or performance decisions

Every business-critical AI suggestion must have human approval status and audit traceability.