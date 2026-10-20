# MFGForge / historical SuperForge source

Earlier Flask/SQLite manufacturing ERP foundation, with linked quality, production, purchasing, quotations, PM and operational reporting features. **Axiom Beta is the current ERP consolidation target**; this repository remains a separate earlier source line.

## Current build state

**Reviewed:** 2026-10-20 · **Inspected main:** `4344adc09f52`.

- [MFGForge Smoke Test](https://github.com/danieloculus0-bot/MFGForge/actions/runs/39489941859) — **Passed** at inspected `main`.

Use [live Actions](https://github.com/danieloculus0-bot/MFGForge/actions) for changes after this dated verification.

## Working implementation

- Runnable local ERP shell, SQLite-backed master data, quality/quoting/planning workspaces and smoke-tested base app.
- Historical SuperForge module source and migration/reference material; existing MFGForge deployments do not automatically migrate to Axiom.
- An independent application smoke workflow, not a newly built integrated Axiom product.

## Run and test

See the [archived complete README](docs/archive/README_2026-10-20_before_refresh.md) for local launch, Windows executable experiments, installer and module guides. Use the repository smoke tests before relying on a build.

## Limitations

- Do not interpret older README claims of MFGForge as canonical ERP integration ownership: **Axiom Beta** supersedes that consolidation role.
- A copied Axiom source snapshot does not equal running cross-database synchronization or installed production software.

## Next steps

Keep archival/historical code compatible while defining explicit data migration and ownership boundaries into Axiom.

## Documentation

- [Current Axiom target](https://github.com/danieloculus0-bot/Axiom_Beta)
- [Full historical README, including original setup detail](docs/archive/README_2026-10-20_before_refresh.md)
