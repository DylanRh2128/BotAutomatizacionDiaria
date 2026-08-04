import os

from fastapi import Header, HTTPException


def verify_webhook_secret(x_webhook_secret: str = Header(default="")):
    if x_webhook_secret != os.environ["WEBHOOK_SECRET"]:
        raise HTTPException(status_code=401, detail="Invalid or missing X-Webhook-Secret")
