# FlowMedic Live — Six-Hour Development Plan

**Status:** Planned; all phases NOT STARTED. Timeboxes are targets, not evidence of completion. The owner should record actual elapsed time and cut scope in the order below if setup or integration delays occur.

For model selection by phase, escalation criteria, and token-efficient context handoffs, use [`MODEL_ROUTING_PLAN.md`](MODEL_ROUTING_PLAN.md). For the Phase 05 visual direction and UI acceptance criteria, use [`UI_DESIGN.md`](UI_DESIGN.md).

## Milestone map

| Phase | Target | Goal | Must-have exit |
|---|---:|---|---|
| 00 Foundation | 0:00–0:25 (25m) | Next.js app shell, env contract, DB migration baseline | App runs; env example and migration strategy exist |
| 01 Real source-to-destination | 0:25–1:20 (55m) | GitHub issues into Neon | Manual sync fetches and upserts real issues |
| 02 Workflow + incidents | 1:20–2:00 (40m) | Persisted run/step/error handling | Real failed DB write becomes incident |
| 03 Repair proposal + validation | 2:00–2:50 (50m) | LLM structured proposal and deterministic safety | Valid proposal shown; unsafe mapping rejected |
| 04 Approval + replay | 2:50–3:35 (45m) | Human gate and idempotent recovery | Approved mapping replays and verifies without duplicates |
| 05 Recovery Studio UI | 3:35–4:35 (60m) | Full-screen node canvas, live step progress, inspector, timeline, approval gate | UI reflects persisted live state end-to-end; see `docs/UI_DESIGN.md` |
| 06 Hardening + deployment | 4:35–5:25 (50m) | Security, errors, Vercel deployment | Preview URL passes critical checks |
| 07 Demo rehearsal + contingency | 5:25–6:00 (35m) | Repeatable judge demo and evidence | Rehearsed flow, fallback, reset instructions |

**Reserve:** phases 06–07 hold 85 minutes (about 24% of total) for integration failures and demo reliability. If behind, keep manual trigger, one repository, one bounded issue page, one schema drift, one mapping, explicit approval, persisted audit, and clear UI. Cut scheduled polling, webhook, extra fields, multi-repository support, and decorative animation first.

## Execution principles

1. Establish one working vertical slice early: one real issue fetched and upserted.
2. Use a dedicated demo DB and migration-controlled schema. Never alter real customer schema.
3. Implement safety before visual polish: allowlist, dry-run validation, human approval, idempotent replay.
4. Each phase ends with evidence recorded in its phase file, the phase log, and changelog.
5. Every new phase starts only after prior exit criteria are met or a clearly documented exception is accepted.

## Phase exit criteria

Detailed checklists live in `docs/PHASES/phase-00.md` through `phase-07.md`. Critical end-to-end acceptance for phase 07:

- Real GitHub issue data appears in isolated Neon Postgres with stable external IDs.
- Controlled column rename causes a real DB undefined-column failure; run/step/incident evidence persists.
- LLM response conforms to a strict structured contract and is treated as untrusted.
- Deterministic allowlist accepts the known mapping and rejects unknown/arbitrary targets.
- No replay occurs before an authenticated human approval of the exact validated proposal.
- Replay succeeds, read-back verification passes, duplicate run does not duplicate rows, and audit timeline shows each action.
- Vercel deployment limits/configuration are checked for actual plan; app behavior remains bounded and resumable.
- Demo rehearsal succeeds twice from clean state, or fallback is explicitly documented.

## Validation cadence

At each phase run the narrowest relevant checks: typecheck/lint/build and targeted unit/integration checks when implemented; database migration checks; API contract checks; then the end-to-end demo. These are planned checks, not completed checks. Record command/test name, environment, outcome, and evidence link or reproducible observation. Do not add a test or claim a check has run without actually doing so.

## Deployment and contingency

Deploy early to a Vercel preview after the core integration is connected. Configure secrets only in Vercel environment settings and local ignored environment files. Confirm DB region/pooler, function region/duration, auth redirect/URL, provider quotas, webhook URL if used, and logs. Never put secrets in the repository or demo recording.

Fallback ladder if external service setup fails:

1. Preserve actual GitHub fetch + actual Postgres write if either integration is available.
2. If LLM unavailable, show an explicitly labeled deterministic known-case proposal, but do not claim AI diagnosis; still use the same validator and human approval.
3. If Vercel deployment fails, demonstrate locally with the same environment and disclose this in the phase log.
4. If live schema mutation is risky or access is unavailable, present a captured real error from a disposable test schema and label the reproduction; do not fabricate an error or point at production.

## Delivery gate

Phase 07 is complete only with a deployed/reproducible demo, checked README setup/runbook, complete phase/changelog records, no leaked secrets, and a final known-limitations list. Any missing external credential or plan feature is a blocker with owner and next action, not an implied success.
