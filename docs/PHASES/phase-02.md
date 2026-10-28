# Phase 02 — Workflow execution and incident capture

**Planned time:** 40 minutes · **Status:** NOT STARTED

## Objective

Persist workflow runs, steps, safe error evidence, and incidents. Demonstrate a genuine PostgreSQL schema-drift failure only in the dedicated demo database.

## Checklist

- [ ] Add migrations for `workflow_steps`, `incidents`, and audit events.
- [ ] Implement state machine and guarded transitions with version checks.
- [ ] Add run/step correlation IDs, duration, status, error class, and safe summaries.
- [ ] Provide explicit demo-only schema rename procedure (migration/manual action) from `issue_title` to `title`.
- [ ] Trigger a fresh sync and capture actual undefined-column SQLSTATE/error.
- [ ] Persist sanitized payload snapshot and incident fingerprint.
- [ ] Add basic incident list/detail read APIs.

## Entrance criteria

- Phase 01 complete; normal sync verified in a disposable database.

## Exit criteria

- Controlled rename causes a real DB failure.
- Incident and failed step persist with safe evidence; no secrets/raw headers logged.
- A retry does not create duplicate incidents for the same failing operation.

## Completion record

- Status: NOT STARTED
- Actual start/end/duration: —
- Implemented: —
- Deviations and decisions: —
- Verification: —
- Evidence: —
- Blockers / owner / next action: —
- Known gaps carried forward: —
