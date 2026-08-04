from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import verify_webhook_secret
from app.classifier import classify_ticket
from app.db import get_db
from app.models import Ticket
from app.schemas import TicketFromEmail, TicketOut

router = APIRouter()


@router.post(
    "/tickets/from-email",
    response_model=TicketOut,
    dependencies=[Depends(verify_webhook_secret)],
)
def create_ticket_from_email(payload: TicketFromEmail, db: Session = Depends(get_db)):
    existing = db.query(Ticket).filter_by(gmail_message_id=payload.message_id).first()
    if existing is not None:
        return existing

    try:
        classification = classify_ticket(subject=payload.subject, body=payload.body)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to classify ticket: {e}")

    ticket = Ticket(
        gmail_message_id=payload.message_id,
        sender_email=payload.sender,
        subject=payload.subject,
        text=payload.body,
        category=classification["category"],
        urgency=classification["urgency"],
        reason=classification["reason"],
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets", response_model=list[TicketOut])
def list_tickets(
    category: str | None = None,
    urgency: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Ticket)
    if category is not None:
        query = query.filter_by(category=category)
    if urgency is not None:
        query = query.filter_by(urgency=urgency)
    return query.order_by(Ticket.created_at.desc()).all()


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    by_category = dict(db.query(Ticket.category, func.count()).group_by(Ticket.category).all())
    by_urgency = dict(db.query(Ticket.urgency, func.count()).group_by(Ticket.urgency).all())
    return {"by_category": by_category, "by_urgency": by_urgency}
