# MFGForge Module Blueprint

This is the active functional scope for MFGForge ERP.

MFGForge must grow into a real manufacturing ERP system, not a fake dashboard. Features should be implemented as durable schemas, usable screens, auditable workflows, and test-covered behavior.

## Required modules

### Quality and customer response

- RMA tracking.
- NCR / DMR / CAPA support.
- Deviation request handling.
- Editable reason codes.
- Customer-linked quality history.
- Work-order-linked quality events.
- Part-linked quality events.

### Work orders and production tracking

- Work order tracking.
- Part linkage.
- Customer linkage.
- Quantity, due date, status, and routing foundations.
- Work order quality traceability.

### FPY and clocking summaries

- FPY summaries from aggregate clocking or completion data.
- First-pass yield by department, work center, part family, customer, and time period.
- Reject/rework visibility without exposing private employee-level data unless explicitly approved.

### Operator efficiency and quoting throughput baselines

- Operator efficiency summaries where allowed by compliant internal data policy.
- Quote throughput baselines.
- Estimated versus actual quoting effort.
- Bottleneck visibility for quoting and engineering review.

### Planning, lead time, and purchasing watchlists

- Planning watchlists.
- Lead-time risk watchlists.
- Purchasing watchlists.
- Supplier/material lead-time visibility.
- Late or at-risk purchasing signals.

### Privacy-safe morale pulse tracking

- Aggregate morale pulse tracking by department.
- Privacy-safe staffing strain indicators.
- Overtime, PTO exhaustion counts, unpaid time off, unscheduled absence counts, turnover counts, and staffing notes.
- Morale treated as an operational risk driver tied to QCDSM.

### Operating setup profile

- Operating mode profile for each shop or tenant:
  - JIT mode.
  - Hybrid mode.
  - Inventory-buffered mode.
- Mode should influence planning, inventory, purchasing, and lead-time risk logic.

### Customer drawing and quote intake

- Customer drawing intake for quoting resources.
- PDF upload/reference record support.
- Automatic PDF BOM candidate extraction from customer drawings.
- BOM candidate review before use.
- No automatic uncontrolled BOM creation from extracted text.

### BOM and material review

- BOM review before use.
- Approved supplier/material catalog entry.
- Controlled material records.
- Supplier linkage.
- Material category, stock form, standard length, unit cost, lead time, and notes.

### Quote material assignment

- Automatic quote material assignment drafts.
- Human review before quote use.
- Material cost estimates.
- Standard length selection.
- Pieces required estimates.
- Lead-time estimates.
- Quote-ready draft calculations without silent approval.

### Dashboard metrics

- ERP command center metrics.
- Quality metrics.
- Delivery risk metrics.
- Purchasing risk metrics.
- Morale pulse metrics.
- Quoting throughput metrics.
- FPY and production performance summaries.

### Editable master data

- Customers.
- Departments.
- Reason codes.
- Suppliers.
- Materials.
- Parts.
- Operating profiles.

## Implementation rules

Build this incrementally.

For every new module:

1. Add or extend durable schema.
2. Expose usable screens/routes.
3. Avoid fake business data.
4. Preserve privacy boundaries.
5. Add or update smoke-test coverage.
6. Commit only passing changes.

## Current next implementation priority

The next practical foundation should be master-data and quoting-related schema expansion:

1. Operating profiles.
2. Approved material catalog.
3. Supplier/material linkage.
4. Quote intake records.
5. PDF BOM candidate records.
6. BOM review status before use.
