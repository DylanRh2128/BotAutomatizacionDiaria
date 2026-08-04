# API Reference

## `POST /tickets/from-email`

Requires header `X-Webhook-Secret` matching the server's `WEBHOOK_SECRET` (`401` if missing or
wrong). Meant to be called by n8n's HTTP Request node.

Body:
```json
{
  "message_id": "abc123",
  "sender": "customer@example.com",
  "subject": "Refund request",
  "body": "My order never arrived, I want a refund."
}
```

Response `200` (also returned unchanged if `message_id` was already seen — idempotent):
```json
{
  "id": 1,
  "created_at": "2026-08-04T12:00:00",
  "gmail_message_id": "abc123",
  "sender_email": "customer@example.com",
  "subject": "Refund request",
  "text": "My order never arrived, I want a refund.",
  "category": "billing",
  "urgency": "high",
  "reason": "Customer is requesting a refund for an undelivered order."
}
```

Errors: `422` if a required field is missing, `502` if the Claude API call fails.

## `GET /tickets`

Query params (optional): `category`, `urgency` — filter the list. Most recent first.

## `GET /tickets/{id}`

Same shape as the webhook response. `404` if the ticket doesn't exist.

## `GET /stats`

```json
{"by_category": {"billing": 3, "technical": 1}, "by_urgency": {"high": 2, "low": 2}}
```
