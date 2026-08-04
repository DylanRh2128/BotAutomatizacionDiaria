# Security

- `DATABASE_URL`, `ANTHROPIC_API_KEY`, and `WEBHOOK_SECRET` are read from environment variables
  (`.env`, loaded via `python-dotenv`). `.env` is git-ignored; only `.env.example` (placeholder
  values) is committed.
- `WEBHOOK_SECRET` should be a long random string (see `.env.example`), not a guessable word —
  it's the only thing stopping a stranger from posting fake tickets to a deployed instance.
- Gmail credentials never touch this repo at all: n8n holds its own Gmail OAuth2 credential,
  entirely outside this codebase.
- `POST /tickets/from-email` is the only endpoint reachable by an external system; `GET`
  endpoints have no auth yet — acceptable for a portfolio demo, a real deployment would add at
  least an API key on the read endpoints too.
