# Phase 02 — Workflow execution and incident capture

**Planned time:** 40 minutes · **Status:** IN PROGRESS

## Objective

Persist workflow runs, steps, safe error evidence, and incidents. Demonstrate a genuine PostgreSQL schema-drift failure only in the dedicated demo database.

## Checklist

- [x] Add a migration for incidents and audit events; Phase 01 already provides the run/step tables, which are extended with correlation and duration fields.
- [x] Implement an incident state machine with guarded transitions and optimistic version checks.
- [x] Add run/step correlation IDs, duration, status, error class, and safe summaries.
- [x] Provide an explicit demo-only SQL procedure to rename `issue_title` to `title` in the disposable Neon database.
- [ ] Trigger a fresh sync and confirm a real undefined-column SQLSTATE `42703` is captured.
- [x] Persist a bounded evidence snapshot and deterministic incident fingerprint without issue bodies or secrets.
- [x] Add protected incident list/detail read APIs with an audit timeline.

## Entrance criteria

- Phase 01 implementation is in place. Phase 02 code was started in parallel with the user's approval while demo service setup is underway; the live failure demonstration still requires the Phase 01 sync and disposable database.

## Exit criteria

- Controlled rename causes a real DB failure.
- Incident and failed step persist with safe evidence; no secrets/raw headers logged.
- A retry does not create duplicate incidents for the same failing operation.

## Completion record

- Status: IN PROGRESS
- Actual start/end/duration: Started 2026-10-28; elapsed time not recorded.
- Implemented: Migration `db/migrations/0002_incidents_audit.sql`; protected incident list/detail APIs; run/step correlation and duration persistence; schema-drift detection and bounded incident capture in `POST /api/runs`; guarded, version-checked incident state transitions; demo-only rename script and runbook in `db/demo/`.
- Deviations and decisions: Phase 02 code was developed in parallel with the remaining live Phase 01 service setup, at the user's direction. The incident captures only SQLSTATE, known relation/column names, bounded issue count/sample numbers, and a stable fingerprint; it does not persist raw database error text or issue bodies.
- Verification: No tests or live-provider checks were run in this implementation pass, per the user's request to keep checks lightweight. The database migration has not been applied and the controlled failure has not been triggered.
- Evidence: Code and migration paths listed above. The expected failure is PostgreSQL undefined-column SQLSTATE `42703`; confirm it through an actual manual sync after applying migrations 0001 and 0002.
- Blockers / owner / next action: Owner: project operator. Apply both migrations to the disposable Neon database after the source repository and credentials are ready; run a normal sync; execute the demo-only rename; run a fresh sync; inspect the incident list/detail APIs and verify repeated failures do not create duplicate incident records for the same run/step/fingerprint.
- Known gaps carried forward: Actual Postgres failure is not yet proven against Neon; approval, AI diagnosis, replay, and the full incident UI are future phases. Migration 0002 is required before the current Phase 01 run handler can persist its extended correlation/audit fields.
