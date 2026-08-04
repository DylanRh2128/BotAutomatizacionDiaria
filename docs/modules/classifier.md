# `app/classifier.py`

Wraps the Anthropic SDK's tool use feature. `classify_ticket()` forces the model to call a
`classify_ticket` tool whose schema restricts `category` and `urgency` to fixed enums, then
re-validates the result server-side (falling back to `other`/`low` on anything unexpected)
before returning it. No free-text JSON parsing anywhere in this module.
