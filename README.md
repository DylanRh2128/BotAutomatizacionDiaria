# Gmail Support Ticket Classifier Bot

> Also reachable at `/support` through this portfolio's `portfolio-gateway` reverse proxy,
> which puts all the portfolio's APIs behind one public URL.

## Problem

A small business gets support requests by email. Nobody has time to tag each one by hand, and
there's no visibility into how many billing vs. technical issues came in this week.

## Solution

A new email triggers n8n's Gmail node, which calls this API's webhook with the email's
content. The API classifies it with an LLM (OpenAI) (category + urgency + a one-line reason) and stores
it, so you get a running history and aggregate stats without touching a spreadsheet.

n8n owns watching Gmail (its Gmail Trigger node handles OAuth and polling); this API owns
classifying and persisting. See [docs/architecture.md](docs/architecture.md) for why the split
is done this way, and [n8n/gmail-ticket-workflow.json](n8n/gmail-ticket-workflow.json) for an
importable example of the n8n side.

## Stack

Python + FastAPI + PostgreSQL (SQLAlchemy) + OpenAI API + n8n (Gmail trigger only).

## How to run it

```bash
python -m venv .venv
.venv/Scripts/activate        # or source .venv/bin/activate on Linux/Mac
pip install -r requirements.txt

cp .env.example .env          # fill in DATABASE_URL, OPENAI_API_KEY, WEBHOOK_SECRET
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API docs.

## Run it with Docker

```bash
OPENAI_API_KEY=your-real-key WEBHOOK_SECRET=your-secret API_KEY=your-read-key docker compose up --build
```

The API is on `http://localhost:8002` (mapped from the container's port 8000). See
[docs/deployment.md](docs/deployment.md) for how to point a locally-running n8n container at it.

## Try it (simulating what n8n would send)

```bash
curl -X POST http://localhost:8000/tickets/from-email \
  -H "X-Webhook-Secret: your-secret" \
  -H "Content-Type: application/json" \
  -d '{"message_id":"abc123","sender":"customer@example.com","subject":"Refund request","body":"My order never arrived, I want a refund."}'
```

Reading tickets back needs the `API_KEY` instead:

```bash
curl -H "X-API-Key: your-read-key" http://localhost:8000/stats
```

## Documentation

- [docs/architecture.md](docs/architecture.md) — n8n vs. API split, webhook auth, junior-acceptable vs. what a senior would do differently
- [docs/api-reference.md](docs/api-reference.md) — endpoints
- [docs/data-model.md](docs/data-model.md) — database schema
- [docs/security.md](docs/security.md) — secrets handling
- [docs/testing.md](docs/testing.md) — what's tested and why
- [docs/deployment.md](docs/deployment.md) — Docker, and reaching this API from a local n8n container
