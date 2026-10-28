-- FlowMedic Phase 01: durable manual sync, execution checkpoints, and GitHub issue destination.
-- Apply using the Neon SQL Editor or an explicitly provisioned migration role.
-- Do not run schema changes using the application's runtime database role.

CREATE TABLE IF NOT EXISTS workflow_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  trigger text NOT NULL CHECK (trigger IN ('manual')),
  repository text NOT NULL,
  status text NOT NULL CHECK (status IN ('running', 'succeeded', 'failed')),
  idempotency_key text NOT NULL UNIQUE,
  started_at timestamptz NOT NULL DEFAULT now(),
  finished_at timestamptz,
  summary text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS workflow_runs_created_at_idx ON workflow_runs (created_at DESC);

CREATE TABLE IF NOT EXISTS workflow_steps (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id uuid NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
  sequence integer NOT NULL CHECK (sequence > 0),
  step_key text NOT NULL CHECK (step_key IN ('fetch_issues', 'upsert_issues')),
  status text NOT NULL CHECK (status IN ('running', 'succeeded', 'failed')),
  started_at timestamptz NOT NULL DEFAULT now(),
  finished_at timestamptz,
  safe_output jsonb,
  error_code text,
  UNIQUE (run_id, sequence),
  UNIQUE (run_id, step_key)
);

CREATE TABLE IF NOT EXISTS github_issues (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source text NOT NULL CHECK (source = 'github'),
  repository text NOT NULL,
  external_id text NOT NULL,
  issue_number integer NOT NULL,
  issue_title text NOT NULL,
  body text NOT NULL DEFAULT '',
  state text NOT NULL CHECK (state IN ('open', 'closed')),
  html_url text NOT NULL,
  source_updated_at timestamptz NOT NULL,
  synced_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (source, repository, external_id)
);

CREATE INDEX IF NOT EXISTS github_issues_repository_updated_idx
  ON github_issues (repository, source_updated_at DESC);
