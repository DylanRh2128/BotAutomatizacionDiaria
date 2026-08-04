# `app/auth.py`

A single FastAPI dependency, `verify_webhook_secret`, used only on
`POST /tickets/from-email`. Compares the `X-Webhook-Secret` header against `WEBHOOK_SECRET` and
raises `401` on any mismatch (including a missing header). Intentionally minimal — this isn't
user authentication, just a way to reject calls that aren't from the configured n8n workflow.
