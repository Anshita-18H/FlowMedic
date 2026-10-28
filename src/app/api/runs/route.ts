import { timingSafeEqual } from "node:crypto";
import { NextResponse } from "next/server";
import {
  createRun,
  finishRun,
  finishStep,
  getIssueCount,
  startStep,
  upsertIssues,
} from "@/lib/database";
import { fetchRepositoryIssues, GitHubRequestError } from "@/lib/github";

export const maxDuration = 30;

function errorResponse(message: string, status: number, correlationId: string) {
  return NextResponse.json(
    { error: { message }, correlationId },
    { status, headers: { "Cache-Control": "no-store" } },
  );
}

function hasValidRunToken(request: Request) {
  const expected = process.env.FLOWMEDIC_RUN_TOKEN?.trim();
  const supplied = request.headers.get("authorization")?.replace(/^Bearer\s+/i, "") ?? "";
  if (!expected || !supplied) return false;
  const expectedBytes = Buffer.from(expected);
  const suppliedBytes = Buffer.from(supplied);
  return expectedBytes.length === suppliedBytes.length && timingSafeEqual(expectedBytes, suppliedBytes);
}

export async function POST(request: Request) {
  const correlationId = crypto.randomUUID();
  if (!process.env.FLOWMEDIC_RUN_TOKEN?.trim()) {
    return errorResponse("Manual runs are disabled until FLOWMEDIC_RUN_TOKEN is configured.", 503, correlationId);
  }
  if (!hasValidRunToken(request)) {
    return errorResponse("Unauthorized.", 401, correlationId);
  }

  const idempotencyKey = request.headers.get("idempotency-key")?.trim();
  if (!idempotencyKey || idempotencyKey.length > 120 || !/^[a-zA-Z0-9._:-]+$/.test(idempotencyKey)) {
    return errorResponse("Send a valid Idempotency-Key header (1–120 letters, digits, . _ : or -).", 400, correlationId);
  }

  const owner = process.env.GITHUB_OWNER?.trim();
  const repositoryName = process.env.GITHUB_REPOSITORY?.trim();
  const token = process.env.GITHUB_TOKEN?.trim();
  if (!process.env.DATABASE_URL?.trim() || !owner || !repositoryName || !token) {
    return errorResponse("Configure DATABASE_URL, GITHUB_TOKEN, GITHUB_OWNER, and GITHUB_REPOSITORY first.", 503, correlationId);
  }

  const repository = `${owner}/${repositoryName}`.toLowerCase();
  let run: Awaited<ReturnType<typeof createRun>>;
  try {
    run = await createRun(idempotencyKey, repository);
  } catch {
    return errorResponse("Could not create a run. Confirm the Phase 01 database migration has been applied.", 503, correlationId);
  }

  if (!run.created) {
    return NextResponse.json(
      { runId: run.id, status: run.status, reused: true, correlationId },
      { status: run.status === "running" ? 202 : 200, headers: { "Cache-Control": "no-store" } },
    );
  }

  let activeStep = "fetch_issues";
  try {
    await startStep(run.id, 1, "fetch_issues");
    const issues = await fetchRepositoryIssues(owner, repositoryName, token);
    await finishStep(run.id, "fetch_issues", "succeeded", { fetchedCount: issues.length });

    activeStep = "upsert_issues";
    await startStep(run.id, 2, "upsert_issues");
    const writtenCount = await upsertIssues(repository, issues);
    const storedCount = await getIssueCount(repository);
    await finishStep(run.id, "upsert_issues", "succeeded", { writtenCount, storedCount });
    await finishRun(run.id, "succeeded", `Fetched ${issues.length}; upserted ${writtenCount}; ${storedCount} stored.`);

    return NextResponse.json(
      { runId: run.id, status: "succeeded", fetchedCount: issues.length, upsertedCount: writtenCount, storedCount, repository, correlationId },
      { headers: { "Cache-Control": "no-store" } },
    );
  } catch (error) {
    const safeMessage = error instanceof GitHubRequestError
      ? error.message
      : error instanceof Error && error.name === "TimeoutError"
        ? "The GitHub request timed out. Retry with a new idempotency key."
        : "The sync failed. Check server logs using the correlation ID.";
    const errorCode = error instanceof GitHubRequestError
      ? `github_${error.status}`
      : error instanceof Error && error.name === "TimeoutError"
        ? "github_timeout"
        : "sync_failed";
    try {
      await finishStep(run.id, activeStep, "failed", { message: safeMessage }, errorCode);
      await finishRun(run.id, "failed", safeMessage);
    } catch {
      // Preserve the original safe failure response if persistence is unavailable.
    }
    return errorResponse(safeMessage, 502, correlationId);
  }
}
