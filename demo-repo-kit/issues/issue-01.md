# Issue 1 — Add retry guidance for temporary timeouts

**Suggested state:** Open  
**Suggested labels:** `integration`, `reliability`

## Body

When the demo importer receives a temporary network timeout, the operator needs a clear retry path.

Acceptance criteria:
- Explain that only transient failures should be retried.
- Preserve the run identifier when showing the error.
- Do not include credentials or request headers in the message.
