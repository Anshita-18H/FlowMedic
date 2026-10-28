# Phase 05 — Recovery Studio workflow canvas

**Planned time:** 60 minutes · **Status:** NOT STARTED

**Design reference:** [`docs/UI_DESIGN.md`](../UI_DESIGN.md)

## Objective

Build a polished operator workspace inspired by node-based workflow canvases: show each real step progressing through the sync and recovery path, with a live execution rail and contextual inspector. Make incident evidence, safe approval, and recovery understandable at a glance.

## Checklist

- [ ] Build responsive dark Recovery Studio shell with accessible contrast, quiet canvas grid, toolbar, and status labels.
- [ ] Render React Flow topology for GitHub → normalize/map → Postgres and a visible incident → diagnose → validate → approval → replay recovery path.
- [ ] Display real active step, elapsed time, finished/failed/queued counts, and factual event sequence; never estimate progress by time.
- [ ] Persist step-start and step-terminal events, and advance one server-authorized bounded step per request.
- [ ] Drive node/edge status from persisted run/step status, not timer-only animation.
- [ ] Add run history, incident detail, sanitized payload/error, diagnosis, and timeline.
- [ ] Add proposal mapping diff, validation evidence, approve/reject confirmation, replay status.
- [ ] Poll run/incident endpoints with bounded backoff and stop on terminal state.
- [ ] Include loading, empty, stale, failure, and permission-denied states.
- [ ] Ensure keyboard operation and clear destructive-action labeling.

## Entrance criteria

- Phases 01–04 provide stable APIs and seeded real workflow states.

## Exit criteria

- Dashboard communicates success, live failure, approval wait, and recovery from real server state.
- Operator can trigger sync, inspect incident, approve/reject, and follow replay.
- Demo UI never implies an unperformed repair succeeded.

## Completion record

- Status: NOT STARTED
- Actual start/end/duration: —
- Implemented: —
- Deviations and decisions: —
- Verification: —
- Evidence: —
- Blockers / owner / next action: —
- Known gaps carried forward: —
