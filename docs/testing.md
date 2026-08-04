# Testing

Run with: `pytest` (needs `DATABASE_URL`, `ANTHROPIC_API_KEY`, `WEBHOOK_SECRET` set to any dummy
value — tests use an in-memory SQLite database and a mocked classifier, never the real Claude
API, and never n8n or Gmail).

- `tests/test_classifier.py` — a valid `tool_use` response parses correctly; an invalid
  category/urgency from the model falls back to `other`/`low` instead of crashing.
- `tests/test_tickets_api.py` — `POST /tickets/from-email` happy path; missing/wrong
  `X-Webhook-Secret` → `401`; the same `message_id` sent twice returns the existing ticket
  without calling the classifier again (asserted via a mock call count); an incomplete payload
  → `422`; `GET /tickets` with and without a filter; `GET /tickets/{id}` including the `404`
  case; `GET /stats` against known data.

n8n itself is never run or tested here — the webhook contract (`docs/api-reference.md`) is what
n8n is expected to call, and `n8n/gmail-ticket-workflow.json` documents that side, but it's a
manual, separate setup step outside this codebase.
