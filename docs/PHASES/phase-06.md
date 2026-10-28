# Phase 06 — Security, hardening, and Vercel deployment

**Planned time:** 50 minutes · **Status:** NOT STARTED

## Objective

Deploy one Vercel project, validate real environment configuration, secure all integration boundaries, and keep all requests bounded and observable.

## Checklist

- [ ] Review every route for auth, authorization, CSRF/origin, validation, size limits, and rate limits.
- [ ] Verify secrets are server-only, absent from client bundle, repo, logs, screenshots, and errors.
- [ ] Verify GitHub webhook HMAC and delivery dedupe if webhook included; protect cron with secret if cron included.
- [ ] Verify DB least privilege, pooler URL, region placement, migration state, and connection pressure.
- [ ] Set service timeouts and function `maxDuration` appropriate to actual Vercel plan.
- [ ] Ensure work persists before response/timeout and can resume; no process-local locks/background assumptions.
- [ ] Configure Vercel env variables separately for preview/production and deploy preview.
- [ ] Review logs, errors, URL/auth redirects, and provider rate limits.
- [ ] Run security and end-to-end checks against disposable services.

## Entrance criteria

- Core demo flow works locally; credentials and Vercel project available.

## Exit criteria

- Preview deployment completes and critical integration flow runs against demo services.
- Actual plan limits and route durations are checked and recorded.
- No secret exposure; failure states are persisted and visible.

## Completion record

- Status: NOT STARTED
- Actual start/end/duration: —
- Implemented: —
- Deviations and decisions: —
- Verification: —
- Evidence: —
- Blockers / owner / next action: —
- Known gaps carried forward: —
