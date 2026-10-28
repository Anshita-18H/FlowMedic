# Database migrations

Store ordered SQL migrations here as `<four-digit-sequence>_<short_name>.sql` (for example `0001_initial_tables.sql`). Apply migrations forward-only, review schema changes before applying, and record the migration version in the database. Runtime application credentials should not be allowed to execute schema changes. The initial application schema will be added in Phase 01; no database schema or credentials are included in Phase 00.
