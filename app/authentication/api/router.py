from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from authentication.dependency_injection.container import get_auth_uc
from authentication.dependency_injection.auth_dependencies import get_current_token


router = APIRouter()

class RegisterIn(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(payload: RegisterIn):
    uc = get_auth_uc()
    try:
        uc.register(payload.email, payload.password)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload: LoginIn):
    uc = get_auth_uc()
    try:
        token = uc.login(payload.email, payload.password)
        return {"token": token}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout(token: str = Depends(get_current_token)):
    uc = get_auth_uc()
    uc.logout(token)
    return {"status": "ok"}

@router.get("/introspect")
def introspect(token: str = Depends(get_current_token)):
    uc = get_auth_uc()
    try:
        return uc.introspect(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
