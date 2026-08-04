from unittest.mock import patch

from tests.conftest import WEBHOOK_SECRET

HEADERS = {"X-Webhook-Secret": WEBHOOK_SECRET}
EMAIL_PAYLOAD = {
    "message_id": "msg-1",
    "sender": "customer@example.com",
    "subject": "I want a refund",
    "body": "My order never arrived and I want my money back.",
}


def test_create_ticket_happy_path(client):
    response = client.post("/tickets/from-email", json=EMAIL_PAYLOAD, headers=HEADERS)
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "billing"
    assert body["gmail_message_id"] == "msg-1"


def test_create_ticket_without_secret_returns_401(client):
    response = client.post("/tickets/from-email", json=EMAIL_PAYLOAD)
    assert response.status_code == 401


def test_create_ticket_with_wrong_secret_returns_401(client):
    response = client.post(
        "/tickets/from-email", json=EMAIL_PAYLOAD, headers={"X-Webhook-Secret": "wrong"}
    )
    assert response.status_code == 401


def test_duplicate_message_id_does_not_reclassify(client):
    client.post("/tickets/from-email", json=EMAIL_PAYLOAD, headers=HEADERS)

    with patch("app.tickets.classify_ticket") as mocked:
        response = client.post("/tickets/from-email", json=EMAIL_PAYLOAD, headers=HEADERS)
        mocked.assert_not_called()

    assert response.status_code == 200
    assert response.json()["gmail_message_id"] == "msg-1"


def test_incomplete_payload_returns_422(client):
    response = client.post(
        "/tickets/from-email", json={"message_id": "msg-2"}, headers=HEADERS
    )
    assert response.status_code == 422


def test_list_tickets_with_filter(client):
    client.post("/tickets/from-email", json=EMAIL_PAYLOAD, headers=HEADERS)

    response = client.get("/tickets", params={"category": "billing"})
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/tickets", params={"category": "technical"})
    assert response.json() == []


def test_get_ticket_by_id_and_404(client):
    created = client.post("/tickets/from-email", json=EMAIL_PAYLOAD, headers=HEADERS).json()

    response = client.get(f"/tickets/{created['id']}")
    assert response.status_code == 200

    response = client.get("/tickets/999")
    assert response.status_code == 404


def test_stats(client):
    client.post("/tickets/from-email", json=EMAIL_PAYLOAD, headers=HEADERS)
    client.post(
        "/tickets/from-email",
        json={**EMAIL_PAYLOAD, "message_id": "msg-2"},
        headers=HEADERS,
    )

    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json() == {"by_category": {"billing": 2}, "by_urgency": {"high": 2}}
