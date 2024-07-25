from fastapi import APIRouter, Depends
from core.auth import authenticate_user, logout_user

auth_router = router = APIRouter(tags=["Auth"])

@router.post("/auth")
def login(credentials: dict = Depends(authenticate_user)) -> dict:
    return {"message": "user logged in successfully"}


@router.post('/logout')
def logout(username: str = Depends(logout_user)):
    return {"message": "user logged out successfully"}