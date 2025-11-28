from pydantic import BaseModel
from datetime import datetime

class InvitationCreate(BaseModel):
    invitee_id: int

class InvitationOut(BaseModel):
    id: int
    group_id: int
    inviter_id: int
    invitee_id: int
    status: str

    class Config:
        orm_mode = True