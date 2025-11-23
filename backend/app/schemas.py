# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}

# GROUP SCHEMAS
class GroupCreate(BaseModel):
    name: str

class GroupOut(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = {"from_attributes": True}

# EXPENSE SCHEMAS
class ExpenseCreate(BaseModel):
    amount: float
    description: str

class ExpenseOut(BaseModel):
    id: int
    amount: float
    description: str
    user_id: int
    group_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

