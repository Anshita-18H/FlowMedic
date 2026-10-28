# Issue 4 — Distinguish closed issues in sync summaries

**Suggested state:** Closed  
**Suggested labels:** `sync`, `reporting`

## Body

The sync summary should preserve whether a source issue is open or closed, so downstream views can distinguish completed work from active work.

Acceptance criteria:
- Store the source state as a bounded value.
- Keep state updates idempotent across repeated syncs.
- Include the state in the operator's record preview.
