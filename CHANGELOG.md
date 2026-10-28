# Changelog

All notable implementation and documentation changes are recorded here. Keep entries factual and tied to phase/evidence. Dates use ISO format.

## Unreleased

- Created the initial implementation-ready architecture, model-routing guidance, phased plan, and UI design documentation.

### 2026-10-28 — Phase 01: Source-to-destination path started

- **Added:** Bounded GitHub Issues fetch/normalization, Neon serverless database access, idempotent issue upserts, run/step persistence, a token-protected `POST /api/runs` endpoint, and a Recovery Studio control that displays configuration and returned sync counts. Added migration `0001_phase_01_source_sync.sql` and `FLOWMEDIC_RUN_TOKEN` to `.env.example`.
- **Changed:** Health readiness now reports Phase 01 service-configuration flags and no longer waits for the later LLM integration.
- **Verified:** No checks or live service sync were run in this implementation pass, per the user's request to avoid extra testing. The GitHub issue endpoint's fine-grained token permission is documented as Issues: read: [GitHub REST issue docs](https://docs.github.com/en/rest/issues/issues).
- **Known issues:** Neon migration and GitHub/Neon credentials are not configured; the UI shows configured environment variables, not verified connectivity. Phase 01 remains in progress.
- **Phase record:** [Phase 01](docs/PHASES/phase-01.md).

### 2026-10-28 — Phase 00: Foundation completed

- **Added:** Next.js App Router foundation, light Recovery Studio shell, loading/error UI states, safe health Route Handler, environment example, and database migration conventions.
- **Changed:** UI plan now records the implemented light shell while keeping the graph, persisted live progress, and full inspector as planned work.
- **Verified:** Formatting, lint, TypeScript, and Webpack production build passed in the implementation session. The user confirmed that the local app and health endpoint check work.
- **Known issues:** GitHub, Postgres, LLM, authentication, and live run orchestration are not implemented; these belong to subsequent phases.
- **Phase record:** [Phase 00](docs/PHASES/phase-00.md).

## Entry format

Use `### YYYY-MM-DD — Phase NN: short title`, then `Added`, `Changed`, `Fixed`, `Verified`, and `Known issues` bullets as applicable. Link the matching phase record. Do not describe planned work as shipped.
