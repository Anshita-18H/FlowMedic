import { NextResponse } from "next/server";
import { hasValidRunToken } from "@/lib/auth";
import { listIncidents } from "@/lib/database";

export async function GET(request: Request) {
  if (!process.env.FLOWMEDIC_RUN_TOKEN?.trim()) {
    return NextResponse.json({ error: { message: "Incident access is not configured." } }, { status: 503 });
  }
  if (!hasValidRunToken(request)) {
    return NextResponse.json({ error: { message: "Unauthorized." } }, { status: 401 });
  }

  const owner = process.env.GITHUB_OWNER?.trim();
  const repositoryName = process.env.GITHUB_REPOSITORY?.trim();
  if (!owner || !repositoryName) {
    return NextResponse.json({ error: { message: "Repository configuration is missing." } }, { status: 503 });
  }

  const requestedLimit = Number(new URL(request.url).searchParams.get("limit") ?? 50);
  const limit = Number.isInteger(requestedLimit) ? Math.max(1, Math.min(100, requestedLimit)) : 50;
  try {
    const incidents = await listIncidents(`${owner}/${repositoryName}`.toLowerCase(), limit);
    return NextResponse.json({ incidents }, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return NextResponse.json(
      { error: { message: "Could not read incidents. Confirm the Phase 02 migration is applied." } },
      { status: 503, headers: { "Cache-Control": "no-store" } },
    );
  }
}
