# steward-api

Resource and operations management (sites, crews, work orders). FastAPI + Postgres CRUD service
with a `work-orders` resource. Owns the `steward` Postgres schema, including its Alembic version table.

Related repos:
- [caldera-platform](https://github.com/prismatic-hq/caldera-platform): CDK, GitOps, shared Helm chart, event contracts
- [applications-infra](https://github.com/prismatic-hq/applications-infra): desired state per environment
- [tremor-api](https://github.com/prismatic-hq/tremor-api): seismic signal streams and alerts service

## Quick Start

Requires `uv`, `task` and Docker.

```sh
task init && task up   # API on http://localhost:8002/docs
```

## Key Commands

| Command | What it does |
|---|---|
| `task init` | Install dependencies and git hooks, create `.env` from `.env.example` |
| `task dev` | Postgres in Docker, API with hot reload |
| `task test` | pytest against real Postgres (testcontainers) |
| `task lint` | ruff lint and format check |
| `task build` | Build the container image |
| `task up` / `task down` | Start / stop the Docker Compose stack |

## Configuration

Database settings come from `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASSWORD`.
Endpoints: `/work-orders`, `/healthz`, `/readyz`, `/metrics`.
Migrations: `uv run alembic upgrade head`.

## Cross-service flow

tremor-api opens one work order per critical alert by calling `POST /work-orders` with
`source_alert_id`. A second work order for the same alert returns 409;
`GET /work-orders?source_alert_id=<uuid>` finds the linked work order.

## CI

Every push and pull request runs lint, tests and a Docker build. Pushes publish to ECR
(`sha-<short-sha>`, `branch-<slug>`, `main`) only when the repo variable `AWS_ROLE_ARN` is set.
