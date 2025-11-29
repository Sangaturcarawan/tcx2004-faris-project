# backend/app/audit/schemas.py

from pydantic import BaseModel
from datetime import datetime

class AuditLogOut(BaseModel):
    id: int
    group_id: int
    user_id: int
    action_type: str
    description: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
