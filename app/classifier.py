import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

CATEGORIES = ["billing", "technical", "shipping", "account", "other"]
URGENCIES = ["low", "medium", "high"]

CLASSIFY_TOOL = {
    "type": "function",
    "function": {
        "name": "classify_ticket",
        "description": "Classify a support ticket by category and urgency.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": CATEGORIES},
                "urgency": {"type": "string", "enum": URGENCIES},
                "reason": {"type": "string", "description": "One short sentence explaining the classification."},
            },
            "required": ["category", "urgency", "reason"],
        },
    },
}

_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-nano")


def classify_ticket(subject: str, body: str, language: str = "en") -> dict:
    reason_language = "Spanish" if language == "es" else "English"
    response = _client.chat.completions.create(
        model=MODEL,
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "function", "function": {"name": "classify_ticket"}},
        messages=[
            {
                "role": "user",
                "content": f"Classify this support ticket. Write the reason in {reason_language}.\n\n"
                f"Subject: {subject}\n\nBody: {body}",
            }
        ],
    )

    tool_call = response.choices[0].message.tool_calls[0]
    result = json.loads(tool_call.function.arguments)

    if result.get("category") not in CATEGORIES:
        logger.warning("Model returned invalid category %r, falling back to 'other'", result.get("category"))
        result["category"] = "other"
    if result.get("urgency") not in URGENCIES:
        logger.warning("Model returned invalid urgency %r, falling back to 'low'", result.get("urgency"))
        result["urgency"] = "low"

    return result
