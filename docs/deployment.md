# Deployment

## Docker (local)

```bash
OPENAI_API_KEY=your-real-key WEBHOOK_SECRET=your-secret docker compose up --build
```

Two containers: `api` (this app, port `8002` on the host) and `db` (`postgres:16-alpine`, port
`5541` on the host, with a healthcheck `api` waits on). `DATABASE_URL` inside
`docker-compose.yml` points at `db:5432` (the Docker network name), separate from the
`localhost`-based `DATABASE_URL` in `.env.example` used when running the app directly on the
host.

## Reaching this API from a local n8n container

If n8n is also running in Docker (e.g. the official `n8nio/n8n` image) on its own network, its
HTTP Request node can't reach this API via `localhost` — `localhost` inside a container means
"that container", not the host machine. Two options:

- **Quick/local demo**: point n8n's HTTP Request node at
  `http://host.docker.internal:8002/tickets/from-email` — `host.docker.internal` is Docker's
  built-in DNS name for the host machine, reachable from any container.
- **Same Docker network**: add n8n's network as an `external` network in this project's
  `docker-compose.yml` and attach the `api` service to it, then n8n can call
  `http://api:8000/tickets/from-email` by service name. Not done by default here, since it would
  make this project's compose file depend on an unrelated one (n8n's) existing — only worth it
  if you're running both together regularly.

## Why Docker, no Kubernetes

Same reasoning as `APIautomatizacionAI`: one service, one database — Kubernetes solves problems
(multi-replica rollout, cluster-wide self-healing) this project doesn't have. Docker Compose is
the right-sized tool.

## Deploying beyond local Docker

The `Dockerfile` is what a platform like Railway or Render would build directly — set
`DATABASE_URL`, `OPENAI_API_KEY`, and `WEBHOOK_SECRET` as environment variables in their
dashboard, and update the n8n workflow's HTTP Request node to the deployed URL.
