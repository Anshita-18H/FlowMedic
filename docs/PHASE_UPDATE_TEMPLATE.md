# Phase update procedure

At the end of every phase, before beginning another:

1. Update the matching `docs/PHASES/phase-NN.md`: status, actual start/end/duration, shipped work, decisions/deviations, verification evidence, failures, blockers, and next action.
2. Update the matching row in `docs/PHASE_LOG.md` with status, actual time, evidence link, and blocker/next action.
3. Add a dated factual entry in `CHANGELOG.md`, linking the phase record. Separate verified behavior from known gaps.
4. Confirm these three records agree. Never backdate evidence; never mark COMPLETE based only on code being written.

## Copyable phase record

```markdown
## Completion record (fill at phase end)
- Status: NOT STARTED | IN PROGRESS | BLOCKED | COMPLETE | DEFERRED
- Actual start/end/duration:
- Implemented:
- Deviations and decisions:
- Verification run (exact check, environment, result):
- Evidence (PR/commit/log/screenshot or reproducible steps):
- Blockers / owner / next action:
- Known gaps carried forward:
```

Use conventional commits such as `docs: add FlowMedic architecture`, `feat(sync): import GitHub issues`, `feat(repair): validate mapping proposals`, and `fix(replay): enforce idempotency`. Prefer small commits at phase boundaries. Include `Phase NN` in the commit body or PR description; do not squash away the phase evidence history.
