import secrets
from fastapi import Depends
from core.config import settings
from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Security
security = HTTPBasic()

# Admin credentials
ADMIN_USERNAME = settings.ADMIN_USERNAME.lower()
ADMIN_PASSWORD = settings.ADMIN_PASSWORD.lower()

# Session management
session = None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    global session
    
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = ADMIN_USERNAME.encode("utf8")
    correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)
    
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = ADMIN_PASSWORD.encode("utf8")
    correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'},
        )
    session = credentials.username
    return session

def logout_user():
    global session
    if session is None:
            return {"message": "Unauthorized"}
    session = None