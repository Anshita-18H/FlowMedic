-- FlowMedic Phase 02: safe incident capture, step timing/correlation, and audit history.
-- Apply after 0001_phase_01_source_sync.sql on the same disposable demo database.

ALTER TABLE workflow_runs
  ADD COLUMN IF NOT EXISTS correlation_id text NOT NULL DEFAULT '';

ALTER TABLE workflow_steps
  ADD COLUMN IF NOT EXISTS correlation_id text NOT NULL DEFAULT '',
  ADD COLUMN IF NOT EXISTS duration_ms integer,
  ADD COLUMN IF NOT EXISTS error_class text;

CREATE TABLE IF NOT EXISTS incidents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id uuid NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
  step_id uuid NOT NULL REFERENCES workflow_steps(id) ON DELETE CASCADE,
  repository text NOT NULL,
  operation text NOT NULL,
  correlation_id text NOT NULL,
  status text NOT NULL DEFAULT 'detected' CHECK (status IN (
    'detected', 'diagnosing', 'proposal_ready', 'validating', 'awaiting_approval',
    'replaying', 'recovered', 'rejected', 'validation_failed', 'replay_failed', 'cancelled'
  )),
  error_code text NOT NULL,
  error_class text NOT NULL,
  fingerprint text NOT NULL,
  safe_summary text NOT NULL,
  evidence jsonb NOT NULL DEFAULT '{}'::jsonb,
  occurrence_count integer NOT NULL DEFAULT 1 CHECK (occurrence_count > 0),
  version integer NOT NULL DEFAULT 1 CHECK (version > 0),
  first_seen_at timestamptz NOT NULL DEFAULT now(),
  last_seen_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (run_id, step_id, fingerprint)
);

CREATE INDEX IF NOT EXISTS incidents_created_at_idx ON incidents (created_at DESC);
CREATE INDEX IF NOT EXISTS incidents_repository_status_idx ON incidents (repository, status, last_seen_at DESC);

CREATE TABLE IF NOT EXISTS audit_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type text NOT NULL CHECK (entity_type IN ('run', 'step', 'incident')),
  entity_id uuid NOT NULL,
  run_id uuid REFERENCES workflow_runs(id) ON DELETE CASCADE,
  correlation_id text NOT NULL,
  action text NOT NULL,
  actor_type text NOT NULL CHECK (actor_type IN ('system', 'operator')),
  details jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS audit_events_entity_timeline_idx ON audit_events (entity_type, entity_id, created_at);
CREATE INDEX IF NOT EXISTS audit_events_run_timeline_idx ON audit_events (run_id, created_at);
