# Phase 00 — Foundation

**Planned time:** 25 minutes · **Status:** COMPLETE

## Objective

Create the Next.js App Router + TypeScript skeleton, initial dashboard shell, env variable contract, database migration baseline, and a working health route. Confirm the project builds and runs locally before integration work.

## Checklist

- [x] Create app using supported current Next.js scaffold and pin package manager/lockfile.
- [x] Add Tailwind base, app layout, light navigation shell, and design tokens. shadcn component adoption is deferred to the UI implementation phase.
- [x] Create `GET /api/health` with safe config-state output and correlation ID; local response confirmed by the user.
- [x] Add `.env.example` containing names only and ignore real environment files.
- [x] Add migration directory and initial migration conventions.
- [x] Add formatting, lint, typecheck, and build scripts.
- [x] Add loading/error and not-connected dashboard states.

## Entrance criteria

- Architecture and decisions reviewed; a dedicated demo GitHub repo and Neon project are planned.

## Exit criteria

- App starts locally and health route responds.
- Build/type checks pass and required env names are documented without values.
- No credentials are tracked; initial migration approach is recorded.

## Completion record

- Status: COMPLETE
- Actual start/end/duration: Started 2026-10-28; elapsed implementation time not recorded. Completion confirmed 2026-10-28.
- Implemented: Next.js App Router project skeleton; light Recovery Studio shell; loading and error states; health Route Handler; `.env.example`; migration conventions; formatting, lint, typecheck, and build scripts. See repository files and [UI design](../UI_DESIGN.md).
- Deviations and decisions: Webpack is selected in the dev/build scripts after the Turbopack CSS pipeline failed in this environment; the Webpack production build passed. shadcn components are deferred to Phase 05, where the full UI is implemented.
- Verification: `npm run format`, `npm run lint`, `npm run typecheck`, and `npm run build` passed in the implementation session. The user subsequently confirmed the local app and `/api/health` check.
- Evidence: Build output included `/`, `/_not-found`, and `/api/health`; the user confirmed the local health check in chat on 2026-10-28. Code is present in `src/app/`, environment contract in `.env.example`, and migration guidance in `db/migrations/README.md`.
- Blockers / owner / next action: None for Phase 00. Proceed to Phase 01.
- Known gaps carried forward: No GitHub, Postgres connection, LLM, authentication, or live run orchestration; no initial database schema; health HTTP response not confirmed. These are tracked for later phases or the remaining Phase 00 check.
