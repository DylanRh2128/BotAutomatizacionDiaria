from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TicketFromEmail(BaseModel):
    message_id: str
    sender: str
    subject: str
    body: str
    language: Literal["en", "es"] = "en"  # language of the one-line reason


class TicketOut(BaseModel):
    id: int
    created_at: datetime
    gmail_message_id: str
    sender_email: str
    subject: str
    text: str
    category: str
    urgency: str
    reason: str

    model_config = {"from_attributes": True}
