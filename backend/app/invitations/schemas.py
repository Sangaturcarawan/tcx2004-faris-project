# app/invitations/schemas.py

from pydantic import BaseModel
from datetime import datetime

class InvitationCreate(BaseModel):
    email: str

class InvitationOut(BaseModel):
    id: int
    group_id: int
    inviter_id: int
    invitee_id: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}