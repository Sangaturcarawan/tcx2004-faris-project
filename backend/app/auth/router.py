# app/auth/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.schemas import UserCreate, UserLogin, UserOut
from app.auth.models import User
from app.auth.utils import create_access_token, decode_access_token, get_current_user
from app.deps import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = bcrypt.hash(user.password)

    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
    

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()

    if not existing or not bcrypt.verify(user.password, existing.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"user_id": existing.id})

    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(user = Depends(get_current_user)):
    return {"message": "Logged out successfully. Token invalidated client-side"}
