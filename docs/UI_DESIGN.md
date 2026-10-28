# FlowMedic Live — Visual UI Plan

**Status:** Light-theme application shell implemented during Phase 00; full Recovery Studio graph, persisted progress, and inspector remain planned for Phase 05.  
**Design goal:** Make FlowMedic feel like a premium workflow operations canvas. The first impression is a connected graph of real systems, and the live run visibly advances across every step. The attached reference informs the spacious node-canvas layout, node detail surfaces, side inspector, and bottom run controls; FlowMedic has its own visual identity and recovery-first hierarchy.

## Product feel

Create a cinematic light-theme “Recovery Studio”: a full-window white workflow canvas with a quiet dot grid, crisp nodes, directional edges, a live execution rail, and a contextual right inspector. Use generous whitespace, fine cool-gray borders, soft blue-violet ambience around the main action, and restrained cobalt/teal progress signals. Success is green, attention is amber, and red is reserved for actual failures. The canvas should feel alive through persisted execution progress and precise motion.

### Visual tokens

| Token | Direction | Use |
|---|---|---|
| Canvas | Cloud `#F5F7FB` with white canvas surface | Page background and workflow area |
| Surface | White `#FFFFFF`, soft panel `#F8FAFF` | Navigation, inspector, run details |
| Hairline | Cool gray `#E5EAF1` | Dividers and graph boundaries |
| Primary signal | Cobalt `#4568E8` | Main action, selected node, setup links |
| Active/integration | Blue/teal `#226DE5` / `#168A9A` | Connected services and in-progress execution |
| Success | Forest green `#178353` | Completed step and verified output |
| Needs attention | Warm amber `#AD6C0A` | Approval required, warning, rate limit |
| Failure | Coral `#CB3D4D` | Actual failed step only |
| Typography | Inter/system UI + mono for IDs/log snippets | Crisp hierarchy and readable technical details |

Use color plus text/icon/shape for every state; never rely on color alone. Keep body text comfortably readable and meet contrast requirements. Honor reduced-motion preference. The implementation is light-only for this hackathon MVP so the canvas and visual hierarchy match the reference direction; do not add an automatic dark-mode switch in Phase 00.

## Main dashboard composition

At desktop size, borrow the reference's workflow-builder composition but make it a recovery command surface:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ FLOWMEDIC / RECOVERY STUDIO   demo-repo  ● connected   [▶ Run workflow] │
├─────────────┬──────────────────────────────────────────────┬─────────────┤
│ TOOL RAIL    │ CANVAS · LIVE RUN  FM-0248          PROGRESS 4/8 │ INSPECTOR │
│ Overview     │                                                  │ Active    │
│ Runs         │ [GitHub] ─▶ [Normalize] ─▶ [Postgres !]          │ Diagnosis │
│ Incidents    │                       └─▶ [Capture] ─▶ [AI ...]   │ Evidence  │
│ Repairs      │                              └▶ [Validate]       │ Mapping   │
│ Settings     │                                  [Approval gate] │ Controls  │
│              │                                                  │           │
├──────────────┴──────────────────────────────────────────────────┴───────────┤
│ EXECUTION RAIL  Fetch ✓  Normalize ✓  Write !  Diagnose ◌  Validate · ... │
│ 00:03 elapsed   current: AI diagnosis · streaming events    [Pause] [Stop] │
└──────────────────────────────────────────────────────────────────────────┘
```

The canvas is the hero: nearly two-thirds of desktop width, pan/zoom, readable node labels, clean branching recovery path, and animated edge pulses only while a real run is active. The side inspector is contextual: selected step details while healthy, incident evidence and approval when repair is needed. The bottom execution rail stays visible during a run, so progress never disappears below the fold. At tablet width, the inspector becomes a bottom sheet or tabbed detail view; at mobile, navigation collapses and the graph becomes a vertical step path with horizontal overflow avoided.

## Workflow topology and visual hierarchy

Show the primary data path left to right across the upper canvas: **GitHub Issues → Normalize → Map & Validate → Neon Postgres**. Attach the recovery path from a failed destination step beneath it: **Capture Incident → Diagnose with AI → Validate Allowlist → Human Approval → Replay & Verify**. A small connector loop can return Replay & Verify to Neon Postgres. Keep the main path and recovery branch readable without requiring users to pan during the judge demo.

Use four node states, each with label, icon/shape, status text, and timing:

| State | Visual treatment | Example in-node evidence |
|---|---|---|
| Queued | Neutral outline, muted connector | `Waiting · —` |
| Running | Cyan leading edge with a restrained animated pulse; compact spinner only in node header | `Fetching issues · 4/12` |
| Succeeded | Lime check mark and a completed connector | `12 records · 2.4s` |
| Failed / attention | Coral error mark for a real failure; amber pause marker for human approval | `SQLSTATE 42703` or `Awaiting approval` |

Do not represent every node with a different accent color. Keep node surfaces consistent; reserve strong state color for the active/failed/success marks and edges. A selected node gets a focus ring and its details appear in the inspector.

## Real progress and loading flow

The execution story should be visible at all times without faking a percentage. At the top of the canvas show the current position (for example `Step 5 of 8`), elapsed time, and current step name. Summarize exact states separately, such as `3 done · 1 failed · 1 active · 3 queued`. Show a segmented progress rail derived from persisted step states; if a percentage is shown, derive it only from known terminal steps and disclose the basis. Never estimate based on time or animate to 100% ahead of the backend.

On each server-side transition, persist a workflow event and step state before updating the UI. The client reads persisted run state/events on a short-interval poll with backoff; the persisted run/event log remains authoritative. For the MVP, the client requests the next server-controlled step only after the previous `advance` response, exposing each real checkpoint without detached serverless work. The event rail should show event time, step label, and factual output (for example `Fetched 12 issues`, `12 normalized`, `Write rejected · undefined column`, `Diagnosis returned`, `Validation passed`, `Approval required`, `Replay verified`). Poll stops at terminal states and resumes after tab focus. On timeout, show `Connection delayed · catching up` and reconcile from server state.

While the current step is running, show a verb-led status in its node and inspector: `Fetching repository issues`, `Normalizing 12 records`, `Writing batch 1/1`, `Asking model for a diagnosis`, `Checking allowed mapping`, or `Verifying replay`. Only show a percentage if that operation reports real measurable progress (such as fetched items). For model calls with no progress event, show the honest state and elapsed time; don't invent a spinner percent.

## Run controls

- **Run workflow:** creates one durable manual run, displays its persisted run ID, then drives one server-authorized bounded step at a time.
- **Pause:** available only between safe checkpoints if execution can honor it; otherwise omit it from MVP.
- **Cancel:** stops future work at the next safe boundary and leaves a clearly marked cancelled run. Never claim an in-flight external request was rolled back.
- **Step details:** clicking a node focuses the inspector and its log segment.
- **Retry:** only appears when server state permits it; schema failures route into incident diagnosis instead of blind retry.
- **Approval gate:** pauses recovery and requires an explicit authenticated approve/reject. Replay action shows exactly which proposal version will execute.

Do not show the familiar play/pause/step controls from the reference unless FlowMedic actually supports those semantics. Run, inspect, approve, and retry are the honest MVP controls.

## Screen and interaction plan

### 1. Recovery Studio / live canvas

- Top bar: FlowMedic mark, environment/repository selector, connection state, user/account, **Run workflow** as the single primary action.
- Compact live-run header: run ID, real step count, elapsed time, current action, and non-estimated progress track.
- Workflow canvas: primary sync chain and visible recovery branch. Nodes show state, duration, factual counts, and selection affordance. Edges show actual direction and live step progression.
- Bottom execution rail: ordered checkpoints; completed, active, failed, awaiting-approval, and queued steps are always distinguishable. Selecting a step opens its inspector details.
- Recent run history appears as a compact chooser/history area, not a competing hero region.
- Helpful empty state: invite operator to connect repository and run the first sync, with a clear setup action.

### 2. Step inspector and incident recovery

This is the key visual moment. When the controlled schema drift occurs, the Postgres node and edge turn coral, the execution rail stops at the failed step, and the inspector opens with the recovery branch and actual progress. The user should see exactly where the flow stopped and what is happening now:

1. **Failure evidence:** “Database rejected column `issue_title`” with the actual sanitized SQLSTATE, time, run ID, and affected step.
2. **What changed:** show expected field versus currently available schema field.
3. **AI diagnosis:** one-sentence root cause, confidence as secondary context, and a clearly labeled AI proposal.
4. **Mapping diff:** `issue_title → title`, with source/target types and allowlist check result.
5. **Validation:** checklist for target exists, required fields covered, types compatible, no duplicate target, dry-run passed.
6. **Human decision:** the graph clearly pauses at an amber approval gate. Approve exact proposal or reject. Primary action says **Approve mapping & replay once**, and includes a concise impact description. No auto-approve or hidden default.

The incident timeline below records actual transitions: detected, diagnosis stored, validation passed, approved by operator, replay completed, row verified.

### 3. Run detail and replay trace

Show each step as a vertical event timeline with timestamps/duration, safe payload preview, request/response summary, and a correlation link. Allow a judge to scrub or select recorded checkpoints after a run; this is inspection of persisted history, not replaying work. Raw secrets, unfiltered bodies, and full authorization-bearing URLs never appear. A failed run links to its incident, not to an unrelated generic error page.

### 4. Repair memory

Show only successful, human-approved mappings. Each entry includes the error/schema fingerprint, mapping, use count, last used, and review state. Label memory as a learned/recorded prior repair—not autonomous authority. Any future use still passes current validation and approval rules.

### 5. Settings / connections

Show GitHub repository identity and permission scope, Postgres connectivity/region status, LLM provider status, trigger options, and diagnostic checks. Display whether a value is configured, never the secret itself. Put optional webhook/poll settings behind a secondary “Advanced” section.

## Micro-interactions and motion

- On run start, a single signal travels along the edge to the currently active node as persisted step events arrive. Stop/retarget animation immediately when state changes.
- The active node receives a restrained moving highlight and a factual verb/status; completed nodes settle into a checkmark and measured duration. Queued nodes stay still.
- The bottom execution rail advances only on persisted events; never use a timer to imply progress.
- On failure, use a quick edge break/pause and node status transition; avoid shaking, flashing, or a fake “AI thinking” spinner detached from a request.
- During diagnosis, show exact status (requesting, proposal received, validating), elapsed time, and a cancel/retry path where supported. The phase label can pulse subtly, but no fabricated percentage appears.
- When approval is needed, freeze the proposal version/hash in the drawer and make the decision buttons explicit.
- On recovery, animate the path to healthy once and reveal verified row identity. Do not loop celebratory effects.
- Use reduced motion and static status as full equivalents.

## Component hierarchy

```text
AppShell
├── PrimaryNav
├── TopBar (workspace, connection state, run action)
├── RecoveryStudioPage
│   ├── RunHeader (run ID, factual step count, elapsed time)
│   ├── WorkflowCanvas (React Flow)
│   │   ├── IntegrationNode (queued/running/succeeded/failed/awaiting approval)
│   │   ├── RecoveryBranch
│   │   └── ExecutionEdge (persisted event state)
│   ├── ExecutionRail (ordered checkpoints + progress)
│   └── StepInspector
│   ├── FailureEvidence
│   ├── DiagnosisSummary
│   ├── MappingDiff
│   ├── ValidationChecklist
│   ├── ApprovalControls
│   └── IncidentTimeline
└── Toast / accessible live announcements
```

## UI acceptance criteria

- [ ] Run graph and bottom execution rail reflect actual persisted server run/step events; no timer-only progress or success simulation.
- [ ] Each step status is persisted by the server before the client requests the next step; interrupted runs resume from stored state.
- [ ] Active step, completed count, elapsed time, and current action remain visible while the run is loading/working.
- [ ] Progress percentage, if present, is derived from known persisted steps or measured item counts; unknown work is labeled as such.
- [ ] The graph presents the sync path and the repair branch in one legible canvas inspired by node-based workflow tools.
- [ ] A judge can understand source, destination, failure, proposed mapping, validation, approval gate, and recovered result without narration.
- [ ] Actual error is visible but sanitized; credentials and raw secrets are absent.
- [ ] Proposal and approval are visually distinct; replay stays unavailable before valid approval.
- [ ] Loading, no connection, empty, running, failed, awaiting approval, recovered, stale, and retry states are designed.
- [ ] Layout works from 320px mobile through large desktop; keyboard, focus, reduced-motion, and contrast are addressed.
- [ ] Every animation is tied to persisted event status and has a static/reduced-motion equivalent.

## Phase 05 build order (60 minutes)

1. 10 min — lock tokens, shell, canvas grid, navigation, node-state language.
2. 20 min — graph topology, recovery branch, persisted progress mapping, execution rail.
3. 20 min — inspector with failure evidence, diagnosis, mapping, validation, approval.
4. 10 min — mobile/reduced-motion/accessibility pass and live demo polish.

If behind schedule, preserve legible graph + incident evidence + approval path. Cut decorative background motion, extra settings, repair-memory browsing, and secondary charts first.

## Front-end guardrails

- Use server state as the source of truth; client state is selection and temporary UI state only.
- Use React Flow for node layout and selection; do not build a general workflow editor in the hackathon scope.
- Use shadcn/ui and Tailwind consistently; add custom visual effects with restraint and no inaccessible low-contrast text.
- Do not create fake metrics or demo success states in the live environment. Label any seeded/example state.

## Implementation note

The current page is a light-theme shell with loading/error UI. Phase 01 adds a manual sync control with environment-configuration indicators, an in-memory masked operator-token field, request state, and returned fetch/upsert/store counts. Those indicators mean values are configured; they do not prove that the provider is reachable. It is not the completed command-center experience described above. The animated workflow, real-time persisted progress, React Flow interactions, incident inspector, and approval flow remain future work; do not present them as implemented until the relevant phase evidence is recorded.
