# PM Native Rebuild Spec

Date: 2026-05-14
Target repo: `danieloculus0-bot/MFGForge`

This is documentation-only planning. It does not change runtime code, schema, tests, packaging scripts, local databases, spreadsheets, or build artifacts.

## Decision

PM Tracking is a behavioral reference only. The preventive maintenance system should be rebuilt natively inside MFGForge/SuperForge as `modules/pm`, not copied from the old PM Tracking app.

## Old PM Tracking reference behavior

Known reference details:

- Local path: `C:\Users\dboone\PM Tracking`
- Launch command: `python -c "exec(open('main.txt', encoding='utf-8').read())"`
- Stack: Flask + openpyxl + sqlite3
- Known files: `pm_data.xlsx`, `pm_app.db`
- Known behavior:
  - dark dashboard UI
  - machine status cards
  - machine detail pages
  - manual operator PM completion entry
  - QR Codes page with printable SVG QR labels
  - Excel export at `/export.xlsx`
  - planned maintenance ticket form

The old app proves the workflow concept. It should not be treated as canonical source code for the ERP module.

## Native module purpose

The native PM module should provide a controlled preventive maintenance and machine-readiness system for SuperForge.

It should support:

- machine and equipment asset tracking
- PM schedule control
- PM completion history
- operator-friendly completion entry
- maintenance ticket/request handling
- QR labels for machine-floor access
- machine status visibility
- overdue PM risk signals
- planning and capacity risk inputs
- Company Pulse maintenance signals
- Excel import/export where appropriate

## Proposed module path

```text
modules/pm/
  __init__.py
  routes.py
  services.py
  qr.py
  exports.py
  models.sql
  templates/
    pm_dashboard.html
    pm_asset_detail.html
    pm_schedule.html
    pm_completion_form.html
    pm_ticket_form.html
    pm_qr_labels.html
```

This path is a target architecture. Do not create it until implementation is explicitly approved.

## Proposed routes

Candidate routes:

- `GET /pm` - PM dashboard with machine status cards and overdue summary
- `GET /pm/assets` - machine/asset list
- `GET /pm/assets/new` - create machine/asset form
- `POST /pm/assets/new` - create machine/asset
- `GET /pm/assets/<asset_id>` - machine detail page
- `GET /pm/assets/<asset_id>/schedule` - PM schedule view
- `POST /pm/assets/<asset_id>/schedule` - add or update PM schedule item
- `GET /pm/assets/<asset_id>/complete` - manual completion form
- `POST /pm/assets/<asset_id>/complete` - record PM completion
- `GET /pm/tickets` - maintenance ticket list
- `GET /pm/tickets/new` - maintenance ticket form
- `POST /pm/tickets/new` - create maintenance ticket
- `GET /pm/qr-labels` - printable QR label page
- `GET /pm/export.xlsx` - Excel export
- `POST /pm/import` - future controlled import path, if needed

## Route safety expectations

QR routes must not allow unauthenticated or accidental destructive actions.

QR labels should open a read-safe asset detail or completion-entry page. Any completion, ticket closure, status change, or schedule change must require a normal POST action and should be auditable.

## Proposed tables

Candidate native tables:

- `pm_assets`
- `pm_schedules`
- `pm_completion_history`
- `pm_tickets`
- `pm_asset_status_snapshots`
- `pm_qr_labels`

Likely relationships:

- `pm_assets.department_id` links to `departments.id`
- `pm_assets.machine_asset_id` may link to `machine_assets.id` if the production machine asset table remains separate
- `pm_completion_history.pm_asset_id` links to `pm_assets.id`
- `pm_completion_history.schedule_id` links to `pm_schedules.id`
- `pm_tickets.pm_asset_id` links to `pm_assets.id`
- `pm_tickets.work_order_id` may optionally link to `work_orders.id`

## Proposed services

Candidate service functions:

- `list_pm_assets()`
- `get_pm_asset(asset_id)`
- `calculate_machine_status(asset_id)`
- `list_due_pm_items(as_of_date)`
- `list_overdue_pm_items(as_of_date)`
- `record_pm_completion(asset_id, schedule_id, completed_by, completed_at, notes)`
- `create_pm_ticket(asset_id, severity, issue, requested_by)`
- `close_pm_ticket(ticket_id, closed_by, close_notes)`
- `build_pm_qr_payload(asset_id)`
- `render_pm_qr_svg(asset_id)`
- `export_pm_xlsx()`
- `import_pm_reference_xlsx()` if imports are later approved

## QR label workflow

The QR label workflow should preserve the old app's practical shop-floor value:

1. Generate one QR label per PM asset or machine.
2. QR target opens the machine detail page or PM completion entry page.
3. Printable page produces simple shop-floor labels.
4. QR payload uses stable internal asset IDs or controlled slugs, not local file paths.
5. QR scan must not directly close PMs or modify records without a form submit.

## Machine status workflow

Machine status cards should show:

- asset number
- asset name
- department
- machine/work-center type
- current status
- last PM date
- next PM date
- overdue status
- open ticket count
- readiness state

Suggested readiness states:

- ready
- due soon
- PM overdue
- down
- limited use
- inspection required

## PM schedule workflow

PM schedules should support:

- PM type
- frequency
- due date calculation
- responsible department or role
- required checks
- last completed date
- next due date
- status

## PM completion workflow

Completion entry should support:

- asset
- schedule item
- completed by
- completed date/time
- pass/fail or completed-with-notes state
- notes
- follow-up ticket creation when a problem is found
- audit timestamp

## Maintenance ticket workflow

Maintenance tickets should support:

- asset
- issue summary
- severity
- requested by
- requested date/time
- assigned to
- status
- downtime impact
- linked work order if applicable
- resolution notes
- closed by
- closed date/time

## Excel import/export expectations

Export should be safe and useful:

- asset register export
- open PM export
- overdue PM export
- completion history export
- ticket export

Imports should be controlled and optional. If the old `pm_data.xlsx` is used as a reference, it must be inspected locally and mapped without committing it.

## Planning and Company Pulse signals

PM should feed planning and intelligence without pretending to be a full scheduling optimizer.

Signals to expose:

- overdue PM count
- machines down
- machines in limited-use state
- high-severity open maintenance tickets
- PM due within planning horizon
- assets with repeated maintenance tickets
- capacity risk caused by machine readiness

Company Pulse should use PM signals as operational risk inputs, not as automatic business decisions.

## Private-data exclusions

Never commit:

- `pm_data.xlsx`
- `pm_app.db`
- old runtime SQLite databases
- local machine history
- employee-level completion records
- shop-private maintenance history
- exported spreadsheets
- QR labels containing private local URLs or machine-specific secrets
- screenshots or reports containing private shop data

## First safe implementation PR

Recommended first implementation PR, after approval:

1. Add empty `modules/pm/` package skeleton.
2. Add route placeholders behind tests.
3. Add schema draft for PM tables.
4. Add smoke tests for read-only PM dashboard route.
5. Do not import old PM data.
6. Do not implement QR write actions yet.

Do not implement the PM module until explicitly approved.