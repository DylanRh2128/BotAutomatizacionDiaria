# `app/classifier.py`

Uses the OpenAI SDK's function calling with a forced `tool_choice`: `classify_ticket()` makes the
model call a `classify_ticket` function whose schema restricts `category` and `urgency` to fixed
enums, then re-validates the result server-side (falling back to `other`/`low` on anything
unexpected) before returning it. The model comes from `OPENAI_MODEL` (default `gpt-5.4-nano`).
No free-text JSON parsing anywhere in this module — only the function call's arguments.
