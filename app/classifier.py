import logging
import os

from anthropic import Anthropic

logger = logging.getLogger(__name__)

CATEGORIES = ["billing", "technical", "shipping", "account", "other"]
URGENCIES = ["low", "medium", "high"]

CLASSIFY_TOOL = {
    "name": "classify_ticket",
    "description": "Classify a support ticket by category and urgency.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "enum": CATEGORIES},
            "urgency": {"type": "string", "enum": URGENCIES},
            "reason": {"type": "string", "description": "One short sentence explaining the classification."},
        },
        "required": ["category", "urgency", "reason"],
    },
}

_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def classify_ticket(subject: str, body: str) -> dict:
    message = _client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=300,
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "classify_ticket"},
        messages=[
            {
                "role": "user",
                "content": f"Classify this support ticket.\n\nSubject: {subject}\n\nBody: {body}",
            }
        ],
    )

    tool_use = next(block for block in message.content if block.type == "tool_use")
    result = dict(tool_use.input)

    if result.get("category") not in CATEGORIES:
        logger.warning("Model returned invalid category %r, falling back to 'other'", result.get("category"))
        result["category"] = "other"
    if result.get("urgency") not in URGENCIES:
        logger.warning("Model returned invalid urgency %r, falling back to 'low'", result.get("urgency"))
        result["urgency"] = "low"

    return result
