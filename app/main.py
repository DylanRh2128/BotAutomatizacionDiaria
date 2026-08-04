from fastapi import FastAPI

from app.db import Base, engine
from app import models  # noqa: F401 — registers models on Base before create_all
from app.tickets import router as tickets_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gmail Support Ticket Classifier Bot")
app.include_router(tickets_router)


@app.get("/health")
def health():
    return {"status": "ok"}
