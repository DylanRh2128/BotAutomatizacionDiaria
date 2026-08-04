from types import SimpleNamespace
from unittest.mock import patch

from app.classifier import classify_ticket


def _fake_response(input_dict):
    tool_use_block = SimpleNamespace(type="tool_use", input=input_dict)
    return SimpleNamespace(content=[tool_use_block])


def test_classify_ticket_valid_response():
    fake = _fake_response({"category": "billing", "urgency": "high", "reason": "Refund request"})
    with patch("app.classifier._get_client") as get_client:
        get_client.return_value.messages.create.return_value = fake
        result = classify_ticket("Refund", "I want a refund")

    assert result == {"category": "billing", "urgency": "high", "reason": "Refund request"}


def test_classify_ticket_invalid_category_falls_back_to_other():
    fake = _fake_response({"category": "not-a-real-category", "urgency": "low", "reason": "x"})
    with patch("app.classifier._get_client") as get_client:
        get_client.return_value.messages.create.return_value = fake
        result = classify_ticket("Subject", "Body")

    assert result["category"] == "other"


def test_classify_ticket_invalid_urgency_falls_back_to_low():
    fake = _fake_response({"category": "billing", "urgency": "urgent!!", "reason": "x"})
    with patch("app.classifier._get_client") as get_client:
        get_client.return_value.messages.create.return_value = fake
        result = classify_ticket("Subject", "Body")

    assert result["urgency"] == "low"
