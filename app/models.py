from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    gmail_message_id: Mapped[str] = mapped_column(String(255), unique=True)
    sender_email: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(20))
    urgency: Mapped[str] = mapped_column(String(10))
    reason: Mapped[str] = mapped_column(Text)
