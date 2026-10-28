# Phase 01 — Real source-to-destination integration

**Planned time:** 55 minutes · **Status:** NOT STARTED

## Objective

Connect a least-privilege GitHub token and managed Postgres; fetch a bounded page of real issues, normalize them, and upsert them with stable keys.

## Checklist

- [ ] Provision dedicated demo repository/database and secrets in local/Vercel settings.
- [ ] Add versioned migrations for `github_issues` and initial target table with `issue_title`.
- [ ] Implement server-only GitHub client with timeout, pagination cap, and rate-limit handling.
- [ ] Exclude pull requests; normalize stable issue fields and bound body length.
- [ ] Implement parameterized Postgres upsert with unique source/repository/external ID.
- [ ] Add authenticated manual `POST /api/runs`; persist run/step start and result.
- [ ] Show connection state and sync result with actual counts.

## Entrance criteria

- Phase 00 complete; credentials available for isolated demo services.

## Exit criteria

- Manual sync fetches actual issues and verifies rows in Neon.
- Repeating same sync updates existing records rather than duplicating.
- Errors are surfaced safely and run state persists.

## Completion record

- Status: NOT STARTED
- Actual start/end/duration: —
- Implemented: —
- Deviations and decisions: —
- Verification: —
- Evidence: —
- Blockers / owner / next action: —
- Known gaps carried forward: —
