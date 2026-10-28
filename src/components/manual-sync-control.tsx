"use client";

import { useEffect, useState, type FormEvent } from "react";

type ServiceReadiness = {
  database: boolean;
  githubToken: boolean;
  repository: boolean;
  runToken: boolean;
};

type SyncResult = {
  runId?: string;
  status?: string;
  fetchedCount?: number;
  upsertedCount?: number;
  storedCount?: number;
  repository?: string;
  error?: { message: string };
};

export function ManualSyncControl() {
  const [open, setOpen] = useState(false);
  const [token, setToken] = useState("");
  const [loading, setLoading] = useState(false);
  const [readiness, setReadiness] = useState<ServiceReadiness | null>(null);
  const [result, setResult] = useState<SyncResult | null>(null);

  useEffect(() => {
    let active = true;
    fetch("/api/health", { cache: "no-store" })
      .then((response) => response.json())
      .then((payload) => {
        if (active && payload.integrations) setReadiness(payload.integrations);
      })
      .catch(() => {
        if (active) setReadiness(null);
      });
    return () => {
      active = false;
    };
  }, []);

  async function startSync(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!token || loading) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("/api/runs", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Idempotency-Key": crypto.randomUUID(),
        },
      });
      const payload = (await response.json()) as SyncResult;
      setResult(response.ok ? payload : { error: payload.error ?? { message: "Sync failed." } });
    } catch {
      setResult({ error: { message: "Could not reach FlowMedic. Check the connection and try again." } });
    } finally {
      setToken("");
      setLoading(false);
    }
  }

  return (
    <div className="sync-control">
      <button className="run-button" type="button" onClick={() => setOpen((value) => !value)}>
        ▶&nbsp; Run workflow
      </button>
      {open && (
        <section className="sync-popover" aria-label="Run a manual GitHub sync">
          <div className="sync-popover-head">
            <div>
              <span className="overline">MANUAL SYNC</span>
              <h2>Run GitHub → Neon</h2>
            </div>
            <button className="sync-close" type="button" onClick={() => setOpen(false)} aria-label="Close">
              ×
            </button>
          </div>

          <div className="sync-connections" aria-label="Service configuration">
            <span className={readiness?.githubToken && readiness.repository ? "configured" : "missing"}>
              <i /> GitHub {readiness?.githubToken && readiness.repository ? "configured" : "setup needed"}
            </span>
            <span className={readiness?.database ? "configured" : "missing"}>
              <i /> Neon {readiness?.database ? "configured" : "setup needed"}
            </span>
          </div>

          <form onSubmit={startSync}>
            <label className="sync-token-label" htmlFor="run-token">
              Operator run token
            </label>
            <input
              id="run-token"
              className="sync-token-input"
              type="password"
              autoComplete="off"
              value={token}
              onChange={(event) => setToken(event.target.value)}
              placeholder="Enter FLOWMEDIC_RUN_TOKEN"
              required
            />
            <p className="sync-hint">Used for this request only; cleared when it finishes.</p>
            <button className="sync-submit" type="submit" disabled={loading || !token}>
              {loading ? <><span className="sync-spinner" /> Syncing issues…</> : "Start manual sync"}
            </button>
          </form>

          {loading && (
            <p className="sync-progress" role="status">
              Sync request is running. FlowMedic saves the fetch and database checkpoints before reporting the result.
            </p>
          )}
          {result?.error && <p className="sync-error" role="alert">{result.error.message}</p>}
          {result?.status === "succeeded" && (
            <div className="sync-success" role="status">
              <strong>Sync complete · {result.repository}</strong>
              <span>{result.fetchedCount} fetched · {result.upsertedCount} upserted · {result.storedCount} stored</span>
              <small>Run {result.runId}</small>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
