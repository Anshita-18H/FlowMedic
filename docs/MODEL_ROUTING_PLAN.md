# Model Routing Plan — FlowMedic Live

**Purpose:** Assign the least expensive suitable model to each development task, reserve stronger reasoning for risk-heavy decisions, and preserve project context in repository docs instead of repeatedly pasting chat history.  
**Status:** Recommended working plan; adjust to the model options actually available in the active Codex environment. Model names and availability can change.

## Recommended phase-to-model map

| Phase | Work | Default model | Reasoning | When to escalate |
|---|---|---|---|---|
| 00 Foundation | Scaffold, scripts, env example, app shell, health endpoint, migration setup | **GPT-6 Luna** | Medium | GPT-6.1 Sol (medium) if framework setup/build errors persist after one focused pass |
| 01 GitHub → Postgres | Straightforward API client, normalization, basic upsert, manual run route | **GPT-6 Luna** | Medium | GPT-6.1 Sol (medium/high) for rate-limit, migration, or serverless connection issues |
| 02 Runs + incidents | Error capture, state machine, persistence, deduplication | **GPT-6.1 Sol** | High | GPT-6 Astra (high) for concurrency/state-transition review or unresolved data-loss behavior |
| 03 AI proposal + validation | Output contract, prompt boundary, deterministic mapping validator, adversarial cases | **GPT-6.1 Terra** | High | **GPT-6 Astra** (high/xhigh) to review safety boundaries and adversarial behavior before merge |
| 04 Approval + replay | Authorization, immutable approval binding, idempotency, safe SQL construction, replay | **GPT-6 Astra** | High | Keep Astra on the security-critical design/review; use Sol for isolated implementation tasks only after the design is fixed |
| 05 Command-center UI | React Flow, incident drawer, timeline, responsive interaction states | **GPT-6.1 Sol** | High for design/interaction; medium for component implementation | GPT-6 Astra for a focused usability/accessibility review if the UI state model becomes complex |
| 06 Hardening + Vercel | Secret handling, webhooks, serverless limits, deployment diagnosis, end-to-end review | **GPT-6 Astra** | High | Astra review remains the final gate for auth/replay/security changes; verify platform facts against official docs |
| 07 Demo rehearsal | Runbook, narration, checklist, known limitations, rehearsal fixes | **GPT-6 Luna** | Medium | GPT-6.1 Sol for cross-system bugs; Astra for final risk review if any approval/security behavior changed |

### Short recommendation

- Use **Luna (Medium)** for Phase 00 and Phase 01, as requested.
- Use **GPT-6.1 Sol** for the bulk of implementation and normal debugging.
- Use **GPT-6.1 Terra** where the work benefits from careful architecture and contract design.
- Reserve **GPT-6 Astra** for the highest-risk decisions and audits: incident state transitions, repair safety, approval/replay, and security/deployment review.
- Do not move every code change to Astra. Keep the design/review task narrow, then delegate bounded implementation to Sol or Luna.

## Task-level routing

Phase names are too broad to determine the best model for every prompt. Split work into short tasks and route by complexity:

| Task characteristics | Route to |
|---|---|
| Mechanical scaffold, small UI component, README/checklist, simple typed API wrapper | Luna, Medium |
| Normal integration, bug fix, moderate refactor, focused component/state wiring | GPT-6.1 Sol, Medium/High |
| Data model, system boundaries, API contract, complex interaction design | GPT-6.1 Terra, High |
| Security-sensitive decisions, approval/replay safety, concurrency invariants, threat review | GPT-6 Astra, High/Xhigh |

Keep the task on its current model when it is making useful progress. Escalate when it encounters repeated ambiguity, changes a security boundary, or cannot explain a data-integrity invariant—not merely because the phase number is higher.

## Token-saving workflow

1. Start each phase with the relevant architecture section, phase checklist, and current `PHASE_LOG.md` row. Do not paste the whole conversation.
2. State the exact task, expected files, constraints, and exit evidence. Ask the model to inspect current code before editing.
3. Keep one model focused on a bounded change. Avoid asking multiple models to rewrite the same files concurrently.
4. Use the stronger model to produce or review a short design/acceptance checklist; use a lower-cost model for routine implementation against that checklist.
5. At handoff, ask for a concise summary: changed files, decisions, checks actually run, unresolved issues, exact next step. Save lasting decisions/evidence to the phase doc and changelog.
6. Start the next phase with repository docs and current code as source of truth; chat history is secondary.
7. Never claim a test/build/deployment succeeded unless it was actually run and the result is recorded.

## Reusable task prompt

```text
Project: FlowMedic Live. Read docs/ARCHITECTURE.md, docs/DEVELOPMENT_PLAN.md,
docs/PHASES/phase-NN.md, and the current docs/PHASE_LOG.md row first.

Task: <one bounded outcome>
Allowed scope: <files/areas>
Must preserve: single Next.js app on Vercel; real GitHub issues and managed
Postgres; AI proposal only; deterministic allowlist; human approval before replay;
idempotent recovery; server-only credentials.
Acceptance: <observable criteria>
Do not: invent completed work, weaken prior phase invariants, add secrets, or
claim checks that you did not run. Inspect existing code and report assumptions.
At completion, report changed files, checks actually run and results, risks,
and the exact next step. Do not update phase status until its exit criteria are met.
```

## Model handoff checklist

- [ ] The current phase document reflects actual implementation and open issues.
- [ ] The next model gets only relevant docs and a concise task prompt.
- [ ] Security decisions and invariants are explicit, not left implicit in chat.
- [ ] The next model is asked to inspect workspace state, not assume a clean tree.
- [ ] Prior checks are described as evidence or unverified; never as assumed success.

## Update policy

Review this plan if model availability, pricing, or task complexity changes. Record changes in `CHANGELOG.md` under a planning entry; this file routes work and does not indicate implementation completion.
