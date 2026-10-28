# Phase 04 — Human approval and safe replay

**Planned time:** 45 minutes · **Status:** NOT STARTED

## Objective

Require an authenticated human to approve the exact validated proposal, then replay once idempotently and verify the destination.

## Checklist

- [ ] Add proposal approval/rejection records and immutable proposal hash.
- [ ] Bind approval to actor, proposal hash, incident version, and validation result.
- [ ] Enforce authenticated action, current state, and stale-version rejection.
- [ ] Generate SQL from code-owned validated identifiers; parameterize issue values.
- [ ] Use original run/issue idempotency key and unique destination key on replay.
- [ ] Bound replay attempt count; reject duplicate or concurrent replay.
- [ ] Read back and verify destination row before marking recovered.
- [ ] Record approval, replay attempt, and terminal outcome in append-only audit.

## Entrance criteria

- Phase 03 complete; dashboard authentication and proposal validation available.

## Exit criteria

- Replay is impossible before approval and impossible for an altered/stale proposal.
- Approved mapping succeeds and verifies; repeating replay creates no duplicate.
- Rejection and replay failure have clear persisted states.

## Completion record

- Status: NOT STARTED
- Actual start/end/duration: —
- Implemented: —
- Deviations and decisions: —
- Verification: —
- Evidence: —
- Blockers / owner / next action: —
- Known gaps carried forward: —
