import { NextResponse } from "next/server";
import { hasValidRunToken } from "@/lib/auth";
import { getIncident } from "@/lib/database";

type RouteContext = { params: Promise<{ incidentId: string }> };

export async function GET(request: Request, context: RouteContext) {
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

  const { incidentId } = await context.params;
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(incidentId)) {
    return NextResponse.json({ error: { message: "Incident not found." } }, { status: 404 });
  }

  try {
    const incident = await getIncident(incidentId, `${owner}/${repositoryName}`.toLowerCase());
    if (!incident) return NextResponse.json({ error: { message: "Incident not found." } }, { status: 404 });
    return NextResponse.json({ incident }, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return NextResponse.json(
      { error: { message: "Could not read incident details. Confirm the Phase 02 migration is applied." } },
      { status: 503, headers: { "Cache-Control": "no-store" } },
    );
  }
}
