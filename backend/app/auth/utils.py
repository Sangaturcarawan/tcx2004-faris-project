# app/auth/utils.py

import jwt
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.models import User


# ===========================
# JWT SETTINGS
# ===========================
SECRET_KEY = "supersecretkey"   # TODO: change to environment variable later
ALGORITHM = "HS256"


# ===========================
# CREATE TOKEN
# ===========================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=12)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ===========================
# DECODE TOKEN
# ===========================
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload      # contains { "user_id": x, "exp": ... }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# ===========================
# GET CURRENT USER FROM TOKEN
# ===========================
auth_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).get(payload["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
