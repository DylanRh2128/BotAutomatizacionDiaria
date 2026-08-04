# Data Model

## `tickets`

| column           | type      | notes                                    |
|------------------|-----------|-------------------------------------------|
| id               | int, PK   |                                           |
| created_at       | datetime  | defaults to now (UTC)                    |
| gmail_message_id | string    | unique — dedupes retried webhook calls   |
| sender_email     | string    |                                           |
| subject          | text      |                                           |
| text             | text      | email body                               |
| category         | string    | one of: billing, technical, shipping, account, other |
| urgency          | string    | one of: low, medium, high                |
| reason           | text      | one-line explanation from Claude          |

Single table — no relations needed for this project.
