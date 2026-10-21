import json
from types import SimpleNamespace
from unittest.mock import patch

from app.classifier import classify_ticket


def _fake_response(input_dict):
    tool_call = SimpleNamespace(function=SimpleNamespace(arguments=json.dumps(input_dict)))
    message = SimpleNamespace(tool_calls=[tool_call])
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def test_classify_ticket_valid_response():
    fake = _fake_response({"category": "billing", "urgency": "high", "reason": "Refund request"})
    with patch("app.classifier._client") as client:
        client.chat.completions.create.return_value = fake
        result = classify_ticket("Refund", "I want a refund")

    assert result == {"category": "billing", "urgency": "high", "reason": "Refund request"}


def test_classify_ticket_invalid_category_falls_back_to_other():
    fake = _fake_response({"category": "not-a-real-category", "urgency": "low", "reason": "x"})
    with patch("app.classifier._client") as client:
        client.chat.completions.create.return_value = fake
        result = classify_ticket("Subject", "Body")

    assert result["category"] == "other"


def test_classify_ticket_invalid_urgency_falls_back_to_low():
    fake = _fake_response({"category": "billing", "urgency": "urgent!!", "reason": "x"})
    with patch("app.classifier._client") as client:
        client.chat.completions.create.return_value = fake
        result = classify_ticket("Subject", "Body")

    assert result["urgency"] == "low"


def test_reason_language_reaches_the_prompt():
    fake = _fake_response({"category": "billing", "urgency": "low", "reason": "x"})
    with patch("app.classifier._client") as client:
        client.chat.completions.create.return_value = fake
        classify_ticket("Subject", "Body", language="es")
    prompt = client.chat.completions.create.call_args.kwargs["messages"][0]["content"]
    assert "Write the reason in Spanish." in prompt
