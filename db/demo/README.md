# Controlled schema-drift demo

This procedure is intentionally destructive to the Phase 01 demo schema. Run it only in the disposable Neon database created for FlowMedic. It renames the destination column that the current sync code expects, creating a real PostgreSQL undefined-column failure (`SQLSTATE 42703`) on the next sync.

1. Confirm that the selected Neon project/branch/database is the isolated FlowMedic demo destination and contains no important data.
2. Confirm `0001_phase_01_source_sync.sql` and `0002_incidents_audit.sql` have been applied.
3. Run [`controlled_schema_drift.sql`](controlled_schema_drift.sql) manually in the Neon SQL Editor.
4. Start a new manual sync. The upsert should fail on the missing `issue_title` field; FlowMedic should mark the step/run failed and persist one `schema_drift` incident with code `42703` and a bounded evidence snapshot.
5. Inspect the incident and audit timeline through the protected incident API or Neon SQL Editor.

This is only the failure demonstration. Phase 03/04 will add safe diagnosis, deterministic allowlist validation, explicit approval, and replay. Do not repair the schema or replay until that later flow is implemented and the operator explicitly approves the action.
