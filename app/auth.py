import os
import secrets

from fastapi import Header, HTTPException


def _matches(given: str, env_var: str) -> bool:
    return secrets.compare_digest(given.encode(), os.environ[env_var].encode())


def verify_webhook_secret(x_webhook_secret: str = Header(default="")):
    if not _matches(x_webhook_secret, "WEBHOOK_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid or missing X-Webhook-Secret")


def verify_api_key(x_api_key: str = Header(default="")):
    if not _matches(x_api_key, "API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")
