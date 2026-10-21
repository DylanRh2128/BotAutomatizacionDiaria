# `app/tickets.py`

The API layer: all four endpoints. `create_ticket_from_email` is the interesting one — it checks
`gmail_message_id` for an existing ticket first (idempotency), only calls `classifier.py` and
commits to the database for genuinely new emails. `list_tickets`/`get_ticket` are plain
SQLAlchemy queries; `get_stats` uses `GROUP BY` in SQL rather than counting in Python or asking
the LLM, since it's simple aggregate arithmetic the database already does well.
