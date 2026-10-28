import "server-only";

import { neon } from "@neondatabase/serverless";
import type { NormalizedIssue } from "@/lib/github";

function getSql() {
  const connectionString = process.env.DATABASE_URL?.trim();
  if (!connectionString) throw new Error("Database is not configured.");
  return neon(connectionString);
}

export async function createRun(idempotencyKey: string, repository: string) {
  const sql = getSql();
  const inserted = await sql`
    INSERT INTO workflow_runs (idempotency_key, trigger, repository, status)
    VALUES (${idempotencyKey}, 'manual', ${repository}, 'running')
    ON CONFLICT (idempotency_key) DO NOTHING
    RETURNING id, status
  `;

  if (inserted.length > 0) {
    return { id: inserted[0].id as string, status: "running" as const, created: true };
  }

  const existing = await sql`
    SELECT id, status FROM workflow_runs WHERE idempotency_key = ${idempotencyKey} LIMIT 1
  `;
  if (!existing[0]) throw new Error("Could not read the idempotent run record.");
  return {
    id: existing[0].id as string,
    status: existing[0].status as string,
    created: false,
  };
}

export async function startStep(runId: string, sequence: number, stepKey: string) {
  const sql = getSql();
  await sql`
    INSERT INTO workflow_steps (run_id, sequence, step_key, status, started_at)
    VALUES (${runId}, ${sequence}, ${stepKey}, 'running', now())
    ON CONFLICT (run_id, step_key) DO UPDATE
      SET status = 'running', started_at = now(), finished_at = NULL, safe_output = NULL
  `;
}

export async function finishStep(
  runId: string,
  stepKey: string,
  status: "succeeded" | "failed",
  safeOutput: Record<string, unknown>,
  errorCode?: string,
) {
  const sql = getSql();
  await sql`
    UPDATE workflow_steps
    SET status = ${status}, finished_at = now(), safe_output = ${JSON.stringify(safeOutput)}::jsonb,
        error_code = ${errorCode ?? null}
    WHERE run_id = ${runId} AND step_key = ${stepKey}
  `;
}

export async function finishRun(runId: string, status: "succeeded" | "failed", summary: string) {
  const sql = getSql();
  await sql`
    UPDATE workflow_runs SET status = ${status}, finished_at = now(), summary = ${summary}
    WHERE id = ${runId}
  `;
}

export async function upsertIssues(repository: string, issues: NormalizedIssue[]) {
  if (issues.length === 0) return 0;

  const sql = getSql();
  const records = issues.map((issue) => ({
    external_id: issue.externalId,
    issue_number: issue.number,
    issue_title: issue.title,
    body: issue.body,
    state: issue.state,
    html_url: issue.htmlUrl,
    source_updated_at: issue.updatedAt,
  }));
  const result = await sql`
    WITH incoming AS (
      SELECT * FROM jsonb_to_recordset(${JSON.stringify(records)}::jsonb) AS issue(
        external_id text, issue_number integer, issue_title text, body text, state text,
        html_url text, source_updated_at timestamptz
      )
    ), written AS (
      INSERT INTO github_issues (
        source, repository, external_id, issue_number, issue_title, body, state, html_url,
        source_updated_at, synced_at
      )
      SELECT 'github', ${repository}, external_id, issue_number, issue_title, body, state,
        html_url, source_updated_at, now() FROM incoming
      ON CONFLICT (source, repository, external_id) DO UPDATE SET
        issue_number = EXCLUDED.issue_number,
        issue_title = EXCLUDED.issue_title,
        body = EXCLUDED.body,
        state = EXCLUDED.state,
        html_url = EXCLUDED.html_url,
        source_updated_at = EXCLUDED.source_updated_at,
        synced_at = now()
      RETURNING 1
    ) SELECT count(*)::integer AS written_count FROM written
  `;
  return Number(result[0]?.written_count ?? 0);
}

export async function getIssueCount(repository: string) {
  const sql = getSql();
  const result = await sql`
    SELECT count(*)::integer AS issue_count FROM github_issues
    WHERE source = 'github' AND repository = ${repository}
  `;
  return Number(result[0]?.issue_count ?? 0);
}
