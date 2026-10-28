# Database migrations

Store ordered SQL migrations here as `<four-digit-sequence>_<short_name>.sql` (for example `0001_initial_tables.sql`). Apply migrations forward-only, review schema changes before applying, and record the migration version in the database. Runtime application credentials should not be allowed to execute schema changes.

## Phase 01 migration

`0001_phase_01_source_sync.sql` creates the run, step, and GitHub issue tables. Apply it once to the dedicated demo database using the Neon SQL Editor while connected to the intended branch/database. Do not paste credentials into chat or commit them. The application runtime role needs only the table privileges required for inserts, updates, and reads; keep DDL privileges with the operator/migration role. Record the applied database, branch, timestamp, and migration filename in the Phase 01 record.
