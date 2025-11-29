# app/members/models.py

from sqlalchemy import (
    Column, 
    Integer, 
    ForeignKey, 
    String, 
    UniqueConstraint)

from app.database import Base
from datetime import datetime

class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="uq_group_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member")
