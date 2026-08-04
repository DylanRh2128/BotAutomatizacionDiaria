from datetime import datetime

from pydantic import BaseModel


class TicketFromEmail(BaseModel):
    message_id: str
    sender: str
    subject: str
    body: str


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
