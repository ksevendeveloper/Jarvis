from datetime import datetime, timedelta
import os

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = os.environ.get("JARVIS_JWT_SECRET", "changeme-jarvis-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


# Simple in-memory user store (replace with DB in production)
_users = {
    "admin": {
        "username": "admin",
        "full_name": "Administrator",
        "hashed_password": pwd_context.hash("admin"),
    }
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    u = _users.get(username)
    if not u:
        return None
    if not verify_password(password, u["hashed_password"]):
        return None
    return User(username=u["username"], full_name=u.get("full_name"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/auth/login", response_model=Token)
async def login(req: LoginRequest):
    user = authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(lambda: None)):
    # This dependency is intended to be used with Header/Depends in endpoints.
    # For simplicity here we return None; more advanced usage is below in docs.
    raise NotImplementedError("Use dependency in-path for protected endpoints")
