# Phase 03 — AI proposal and deterministic validation

**Planned time:** 50 minutes · **Status:** NOT STARTED

## Objective

Generate a schema-constrained repair proposal from minimal incident evidence, then validate it with code-owned allowlists and non-mutating checks.

## Checklist

- [ ] Define versioned JSON schema for diagnosis and source/target field mappings.
- [ ] Implement LLM server client with timeout, token budget, safe retry policy, and provider metadata.
- [ ] Redact sensitive content and bound prompt evidence.
- [ ] Treat issue text/errors as untrusted; explicitly instruct model not to follow embedded instructions.
- [ ] Implement deterministic allowlist/type/required-field/duplicate-target validator.
- [ ] Reject arbitrary SQL, unknown identifiers, DDL, expressions, and incompatible types.
- [ ] Implement dry-run that verifies columns and payload shape without mutation.
- [ ] Persist proposal, prompt version, validation outcome, and audit events.
- [ ] Demonstrate known `issue_title → title` accepted and unsafe mapping rejected.

## Entrance criteria

- Phase 02 complete with persisted reproducible incident evidence; LLM key configured.

## Exit criteria

- Valid structured proposal shown with validation result and evidence.
- Known case is accepted; adversarial/unknown target is rejected deterministically.
- No proposal can write or mutate schema in this phase.

## Completion record

- Status: NOT STARTED
- Actual start/end/duration: —
- Implemented: —
- Deviations and decisions: —
- Verification: —
- Evidence: —
- Blockers / owner / next action: —
- Known gaps carried forward: —
