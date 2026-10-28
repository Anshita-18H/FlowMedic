# Issue 6 — Prevent duplicate records on repeated sync

**Suggested state:** Open  
**Suggested labels:** `reliability`, `data`

## Body

Running the same repository sync multiple times should update existing destination records instead of inserting duplicates.

Acceptance criteria:
- Use the repository and stable GitHub issue ID as the unique source key.
- Refresh changed title, state, body, URL, and source update time.
- Keep the stored row count stable when the source issue set has not changed.
