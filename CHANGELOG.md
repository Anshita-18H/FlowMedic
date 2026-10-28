# Changelog

All notable implementation and documentation changes are recorded here. Keep entries factual and tied to phase/evidence. Dates use ISO format.

## Unreleased

- Created the initial implementation-ready architecture, model-routing guidance, phased plan, and UI design documentation.

### 2026-10-28 — Phase 00: Foundation started

- **Added:** Next.js App Router foundation, light Recovery Studio shell, loading/error UI states, safe health Route Handler, environment example, and database migration conventions.
- **Changed:** UI plan now records the implemented light shell while keeping the graph, persisted live progress, and full inspector as planned work.
- **Verified:** Formatting, lint, TypeScript, and Webpack production build passed in the implementation session. The local HTTP health response could not be confirmed because local socket access was unavailable.
- **Known issues:** Phase 00 remains in progress until its outstanding verification and acceptance criteria are resolved. Integrations and authentication are not implemented.
- **Phase record:** [Phase 00](docs/PHASES/phase-00.md).

## Entry format

Use `### YYYY-MM-DD — Phase NN: short title`, then `Added`, `Changed`, `Fixed`, `Verified`, and `Known issues` bullets as applicable. Link the matching phase record. Do not describe planned work as shipped.
