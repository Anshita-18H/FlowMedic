# Issue 3 — Keep issue links available in the destination

**Suggested state:** Open  
**Suggested labels:** `data`, `traceability`

## Body

Each imported issue should retain its original GitHub URL so the operator can open the source record while reviewing a sync result.

Acceptance criteria:
- Store the canonical issue URL.
- Make the URL available in the sanitized issue summary.
- Do not construct links from untrusted text.
