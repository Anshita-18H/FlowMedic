# Phase 00 — Foundation

**Planned time:** 25 minutes · **Status:** IN PROGRESS

## Objective

Create the Next.js App Router + TypeScript skeleton, initial dashboard shell, env variable contract, database migration baseline, and a working health route. Confirm the project builds and runs locally before integration work.

## Checklist

- [x] Create app using supported current Next.js scaffold and pin package manager/lockfile.
- [x] Add Tailwind base, app layout, light navigation shell, and design tokens. shadcn component adoption is deferred to the UI implementation phase.
- [x] Create `GET /api/health` with safe config-state output and correlation ID. The handler compiles; its local HTTP response remains unconfirmed.
- [x] Add `.env.example` containing names only and ignore real environment files.
- [x] Add migration directory and initial migration conventions.
- [x] Add formatting, lint, typecheck, and build scripts.
- [x] Add loading/error and not-connected dashboard states.

## Entrance criteria

- Architecture and decisions reviewed; a dedicated demo GitHub repo and Neon project are planned.

## Exit criteria

- App starts locally; health route HTTP response still needs confirmation.
- Build/type checks pass and required env names are documented without values.
- No credentials are tracked; initial migration approach is recorded.

## Completion record

- Status: IN PROGRESS
- Actual start/end/duration: Started 2026-10-28; elapsed implementation time not recorded.
- Implemented: Next.js App Router project skeleton; light Recovery Studio shell; loading and error states; health Route Handler; `.env.example`; migration conventions; formatting, lint, typecheck, and build scripts. See repository files and [UI design](../UI_DESIGN.md).
- Deviations and decisions: Webpack is selected in the dev/build scripts after the Turbopack CSS pipeline failed in this environment; the Webpack production build passed. shadcn components are deferred to Phase 05, where the full UI is implemented.
- Verification: `npm run format`, `npm run lint`, `npm run typecheck`, and `npm run build` passed in the implementation session. The production server reported ready. A local HTTP request to `/api/health` could not be completed because socket access was unavailable; do not treat endpoint behavior as verified.
- Evidence: Build output included `/`, `/_not-found`, and `/api/health`; see the implementation-session results. Code is present in `src/app/`, environment contract in `.env.example`, and migration guidance in `db/migrations/README.md`.
- Blockers / owner / next action: No product blocker. Reconfirm `/api/health` via an available local runtime, then review remaining Phase 00 exit criteria.
- Known gaps carried forward: No GitHub, Postgres connection, LLM, authentication, or live run orchestration; no initial database schema; health HTTP response not confirmed. These are tracked for later phases or the remaining Phase 00 check.
