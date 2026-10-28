const requiredConfiguration = ["DATABASE_URL", "GITHUB_TOKEN", "LLM_API_KEY"] as const;

export function GET(request: Request) {
  const incomingId = request.headers.get("x-correlation-id");
  const correlationId =
    incomingId && /^[a-zA-Z0-9._:-]{1,80}$/.test(incomingId) ? incomingId : crypto.randomUUID();
  const configured = requiredConfiguration.every((name) => Boolean(process.env[name]?.trim()));

  return Response.json(
    {
      status: "ok",
      readiness: configured ? "configured" : "setup_required",
      correlationId,
      timestamp: new Date().toISOString(),
    },
    { headers: { "Cache-Control": "no-store" } },
  );
}
