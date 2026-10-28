# FlowMedic Live

**When automations break, ours help them recover.**

FlowMedic Live is a Vercel-deployable Next.js application for showing real workflow execution and safely recovering from supported integration failures. The first demo path reads GitHub issues, stores them in managed Postgres, detects a controlled schema mismatch, proposes an allowlisted repair, waits for human approval, and verifies an idempotent replay.

## Current status

Phase 00 foundation is **in progress** and recorded in [`docs/PHASES/phase-00.md`](docs/PHASES/phase-00.md). The light Recovery Studio shell, safe health endpoint, project scripts, environment contract, and migration conventions are in place. Formatting, lint, TypeScript, and production build checks passed. The local HTTP response from `/api/health` has not yet been confirmed in this environment. GitHub, Postgres, LLM, authentication, and live step execution are not connected yet.

## Run locally

Requirements: Node.js 20.9 or newer and npm 11.19.0 (or compatible npm 11).

```powershell
npm ci
Copy-Item .env.example .env.local
npm run dev
```

Open `http://localhost:3000`. The starter environment file contains variable names with blank values. Add real values only to `.env.local` or the deployment provider’s server-side environment settings; never commit credentials. The health endpoint is available at `/api/health` and returns liveness, a coarse setup state, a correlation ID, and a timestamp without returning secret values.

## Useful commands

```text
npm run dev        Start the local development server
npm run lint       Run ESLint
npm run typecheck  Check TypeScript types
npm run build      Create a production build
npm start          Run the production build locally
```

## Project map

```text
src/app/                 Next.js App Router pages and Route Handlers
src/app/api/health/       Safe liveness/configuration endpoint
db/migrations/            Forward-only SQL migration conventions
docs/                     Architecture, phase plan, decisions, and evidence log
```

## Project documents

- [Architecture](docs/ARCHITECTURE.md)
- [Six-hour development plan](docs/DEVELOPMENT_PLAN.md)
- [Model routing and token plan](docs/MODEL_ROUTING_PLAN.md)
- [Light Recovery Studio UI plan](docs/UI_DESIGN.md)
- [Phase log](docs/PHASE_LOG.md)
- [Phase 00 implementation record](docs/PHASES/phase-00.md)
- [Changelog](CHANGELOG.md)

At the end of every phase, update its phase record, `docs/PHASE_LOG.md`, and `CHANGELOG.md` before beginning the next phase. Record only checks actually run and results actually observed.
