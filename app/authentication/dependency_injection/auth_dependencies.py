from typing import Optional
from fastapi import Header, HTTPException
from authentication.dependency_injection.container import get_auth_uc

def get_current_token(
    authorization: Optional[str] = Header(None),
    auth: Optional[str] = Header(None, alias="Auth"),
):
    raw = authorization or auth
    if not raw:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = raw.split(" ", 1)[1].strip() if raw.lower().startswith("bearer ") else raw.strip()

    uc = get_auth_uc()
    if not uc.validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
