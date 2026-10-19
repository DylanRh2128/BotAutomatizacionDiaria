# `app/auth.py`

Two FastAPI dependencies, both raising `401` on any mismatch (including a missing header):

- `verify_webhook_secret` — on `POST /tickets/from-email`. Compares `X-Webhook-Secret` against
  `WEBHOOK_SECRET`. Not user authentication, just a way to reject calls that aren't from the
  configured n8n workflow.
- `verify_api_key` — on every `GET` endpoint. Compares `X-API-Key` against `API_KEY`, so reading
  stored emails needs a different secret than posting them.

Comparisons use `secrets.compare_digest` (constant time).
