# Architecture

## Flow

New email → n8n's Gmail Trigger node fires → n8n's HTTP Request node calls
`POST /tickets/from-email` with the extracted fields → `app/classifier.py` classifies with
OpenAI (function calling) → `app/tickets.py` persists a `Ticket` row → response returned to n8n (ignored
by the workflow, but useful for manual testing/`curl`).

## Why n8n handles Gmail, not this code

Reading Gmail requires OAuth2 (or IMAP + an app password) and ongoing polling. n8n's Gmail
Trigger node already does this reliably with a GUI credential flow — reimplementing it in Python
would be solving a problem n8n has already solved well, for no benefit to a portfolio piece
about backend APIs. The Gmail credential lives inside n8n, never in this repo: this API doesn't
know Gmail exists, it only knows "someone sends me `{message_id, sender, subject, body}`".

## Why this endpoint has a shared-secret header (unlike `APIautomatizacionAI`)

`APIautomatizacionAI`'s endpoints were left without auth as a documented MVP gap, meant to be
tried manually/locally. This webhook is different: it's meant to sit on the public internet so
n8n can reach it, which means anyone who finds the URL could otherwise post fake tickets. A
shared secret (`X-Webhook-Secret` header, checked against `WEBHOOK_SECRET`) is the minimum bar
for an endpoint that's actually meant to be called by an automated third party over the internet.

## Classification: tool use, not "please respond in JSON"

`app/classifier.py` defines a `classify_ticket` tool with a JSON Schema that constrains
`category` to 5 fixed values and `urgency` to 3 fixed values, and forces the model to call that
tool (`tool_choice`). This is read directly from the `tool_use` content block — no parsing of
free-form text, no risk of the model wrapping its answer in markdown or extra prose.

Even so, the code re-validates `category`/`urgency` against the allowed lists before saving,
falling back to `other`/`low` with a logged warning if something doesn't match. Tool use makes
a schema violation unlikely, not impossible — never trust an LLM's output to enforce your
database's constraints for you.

## Idempotency

`gmail_message_id` is unique. If n8n retries a webhook call (network hiccup, workflow re-run),
`POST /tickets/from-email` returns the existing ticket instead of creating a duplicate or
calling the LLM a second time for the same email.

## Junior-acceptable vs. what a senior would do differently

- **Schema management**: `Base.metadata.create_all()` on startup, no Alembic — same tradeoff as
  `APIautomatizacionAI`, kept consistent across the portfolio's shared stack.
- **Single shared secret, not per-workflow keys**: fine for one n8n workflow calling one API; a
  senior supporting multiple external callers would issue a distinct key per caller so one can
  be revoked without breaking the others.
- **No retry on OpenAI API failures**: a transient failure returns a 502 and the email is simply
  never marked processed by n8n's workflow (so it can be manually resent); a senior would add a
  bounded retry with backoff before giving up.
