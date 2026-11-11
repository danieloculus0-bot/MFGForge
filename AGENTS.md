# MFGForge Agent Instructions

## Active project

MFGForge is a historical Flask/SQLite ERP source line. Axiom_Beta is the active ERP consolidation target. Maintain this repository as a runnable reference and migration source; do not claim it is synchronized with Axiom.

Repo: `danieloculus0-bot/MFGForge`

This is not PM-Tracker, ForgeQC, EZ-FAIR, ForgeVault, venvWin, LAYR, or any other side project. Those projects may provide module history, lessons, or reusable ideas. For new cross-module ERP integration, inspect Axiom_Beta first and coordinate changes through its existing interfaces.

## Product purpose

Build a practical manufacturing ERP system for small and mid-size fabrication and contract manufacturing shops.

The system should feel like real manufacturing software, not a toy demo dashboard. It should prioritize usable workflows, real records, clear navigation, auditability, and manufacturing decision support.

Core direction:

- Manufacturing ERP foundation.
- Quality management built in, not bolted on.
- QCDSM-centered operations: Quality, Cost, Delivery, Safety, Morale.
- Morale is treated as an operational driver tied to quality, delivery, overtime, staffing pressure, attendance trends, PTO exhaustion, turnover, and shop strain.
- AI assistance should behave like GPS, not a self-driving car. It assists humans, suggests actions, drafts records, summarizes risk, and runs common approved tasks. It must not silently make business-critical decisions.

## Required workflow behavior

Always inspect the real repository files before proposing or applying patches.

Do not invent paths, APIs, modules, tables, or fake data.

Do not blindly rewrite the project.

Do not create misleading placeholder demo records or real customer/manufacturing data. When tests require records, use clearly labeled, wholly synthetic fictional fixtures.

Make grounded edits based only on actual files in the repo.

Fix one issue at a time.

Prefer full working replacement files when a file needs substantial edits.

Avoid tiny unexplained snippets.

Do not push commits unless Daniel explicitly asks or has already granted write permission in the current task.

When uncertain, inspect first.

## Local command style for user-facing instructions

When giving Daniel local commands, use one self-contained PowerShell block.

The block should:

- Define useful variables such as `$repo`.
- Find or set the correct project path automatically.
- Create needed folders or files with PowerShell when appropriate.
- Print clear next-action text with `Write-Host`.
- End with a short prompt telling Daniel what to report back.

Do not give long multi-step command lists.

## UI direction

Use a professional manufacturing ERP style:

- Dark, clean, tactical.
- Practical shop-floor readability.
- Clear navigation.
- Useful status panels.
- Minimal bullshit.

Avoid:

- Toy dashboard feel.
- Fake cyberpunk styling.
- Rainbow buttons.
- Neon gimmicks.
- Placeholder app vibes.

## Expected ERP modules

MFGForge may eventually include:

- Customers and suppliers.
- Part master.
- BOM and routing.
- Work orders.
- Inventory.
- Purchasing.
- Planning and scheduling.
- Preventive maintenance.
- First Article Inspection / FAIR generation.
- RMA tracking.
- NCR / DMR / deviation handling.
- Corrective action and 5-Why support.
- Quality metrics and reporting.
- Document control / PDM tie-in.
- Audit trail.
- Morale and operational strain indicators.
- AI assistant layer with approval-gated actions.

Do not assume all modules already exist. Inspect the repo first.

## AI assistant rules

AI features must be human-in-the-loop.

Preferred pattern:

1. Read-only analysis first.
2. Draft recommendation or action.
3. Human approval.
4. Logged execution.
5. Audit trail.

Safe AI tasks:

- Summarize trends.
- Draft RMA/NCR/CAPA language.
- Flag risk patterns.
- Explain ERP records.
- Suggest next actions.
- Generate reports from approved data.
- Prepare forms and exports.

Unsafe AI tasks without approval:

- Closing quality records.
- Changing inventory.
- Releasing jobs.
- Approving deviations.
- Editing customer records.
- Sending external emails.
- Making employment/personnel decisions.

## Data and privacy rules

Never commit proprietary customer drawings, real RMA events, customer names, defect logs, quote PDFs, private Excel trackers, exports, local databases, attendance data, or company-private records.

Morale and attendance metrics must remain aggregate-only by department, role group, or period. Do not store employee-level identifiers unless Daniel explicitly creates a compliant internal data model for it.

Use seed data only when it is clearly labeled synthetic and necessary for development. Prefer empty schemas and import paths over fake business records.

## Development standard

Build toward deployable software, not mockup theater.

Every added feature should either:

- Run.
- Have a clear schema.
- Have a usable route/view/API.
- Have a test or smoke-test path.
- Move the product closer to a real ERP foundation.

If the repo is empty or minimal, start by creating the smallest useful real foundation: app entrypoint, requirements, data layer, durable schema, navigation shell, and smoke test.


## Mandatory confidentiality boundary for all contributors and automated agents

Never publish nonpublic employer, client, supplier or contractor information, including company-specific work details, names and branding, real equipment or maintenance inventories, HR/personnel data, customer records, job and ERP exports, RMAs, quality investigations, drawings, site configuration, credentials or private operational procedures. Never copy material from work drives or private conversations to source, branches, messages, pull requests, issues, GitHub Pages, Actions logs or artifacts. Use only neutral, fully synthetic examples when examples are needed. Review every change for confidentiality before publishing; if release authorization is uncertain, exclude it. Removing files from a current branch does not erase commit history. This applies even when another agent recommends publication.
