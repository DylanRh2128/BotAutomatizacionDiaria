# Security

- `DATABASE_URL`, `OPENAI_API_KEY`, and `WEBHOOK_SECRET` are read from environment variables
  (`.env`, loaded via `python-dotenv`). `.env` is git-ignored; only `.env.example` (placeholder
  values) is committed.
- `WEBHOOK_SECRET` should be a long random string (see `.env.example`), not a guessable word —
  it's the only thing stopping a stranger from posting fake tickets to a deployed instance.
- Gmail credentials never touch this repo at all: n8n holds its own Gmail OAuth2 credential,
  entirely outside this codebase.
- `POST /tickets/from-email` needs `WEBHOOK_SECRET`; the `GET` endpoints (which expose stored
  senders and email bodies) need a separate `API_KEY`. Both are compared with
  `secrets.compare_digest` so response timing doesn't leak how much of a guess was right.
