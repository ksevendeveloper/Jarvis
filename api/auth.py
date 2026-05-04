from datetime import datetime, timedelta
import os

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt

from sqlalchemy.orm import Session
from db import get_db
from api import models as orm_models

SECRET_KEY = os.environ.get("JARVIS_JWT_SECRET", "changeme-jarvis-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

router = APIRouter()
security = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token():
    return jwt.encode({"rnd": os.urandom(16).hex()}, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/auth/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(orm_models.User).filter(orm_models.User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token()
    # persist refresh token
    try:
        rt = orm_models.RefreshToken(user_id=user.id, token=refresh_token)
        db.add(rt)
        db.commit()
    except Exception:
        db.rollback()
        refresh_token = None
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post('/auth/refresh', response_model=Token)
def refresh_token(req: RefreshRequest, db: Session = Depends(get_db)):
    rt = db.query(orm_models.RefreshToken).filter(orm_models.RefreshToken.token == req.refresh_token).first()
    if not rt:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.query(orm_models.User).filter(orm_models.User.id == rt.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": req.refresh_token}


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(orm_models.User).filter(orm_models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
