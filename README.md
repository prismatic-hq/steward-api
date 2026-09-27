# steward-api

Resource and operations management (sites, crews, work orders). FastAPI + Postgres CRUD service
with a `work-orders` resource. Owns the `steward` Postgres schema, including its Alembic version table.

Related repos:
- [caldera-platform](https://github.com/prismatic-hq/caldera-platform): CDK platform, `preview` CLI, services Helm chart, event contracts
- [tremor-api](https://github.com/prismatic-hq/tremor-api): seismic signal streams and alerts service

## Quick Start

Requires [mise](https://mise.jdx.dev/getting-started.html) and Docker (mise installs Python and uv).

```sh
mise trust && mise install && mise run init && mise run up # API on http://localhost:8002/docs
```

## Key Commands

| Command | What it does |
|---|---|
| `mise run init` | Install dependencies and git hooks, create `.env` from `.env.example` |
| `mise run dev` | Postgres in Docker, API with hot reload |
| `mise run test` | pytest against real Postgres (testcontainers); extra args go to pytest |
| `mise run lint` | ruff lint and format check |
| `mise run build` | Build the container image |
| `mise run up` / `mise run down` | Start / stop the Docker Compose stack |

## Configuration

Database settings come from `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASSWORD`.
Endpoints: `/work-orders`, `/healthz`, `/readyz`, `/metrics`.
Migrations: `uv run alembic upgrade head`.

## Cross-service flow

tremor-api opens one work order per critical alert via `source_alert_id`; a duplicate is a
409, and `GET /work-orders?source_alert_id=<uuid>` finds it.

## CI

Every push runs lint, tests and one multi-arch (amd64, arm64) image build in parallel jobs; pull
requests run them only when they come from forks. When the repo variable `AWS_ROLE_ARN` is set,
pushes publish `sha-<short-sha>` (plus `main` on `main`) to ECR with a BuildKit registry cache, and
skip the build when that tag already exists. Fork code never gets AWS credentials.

## Preview environments

Non-`main` pushes call caldera-platform `preview-environment.yml` twice: in parallel with the build,
then after the image push. Branch deletion calls `preview-environment-teardown.yml`. Never forks.
