# backend/app/audit/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action_type = Column(String, nullable=False)  # e.g. "expense_created"
    description = Column(Text, nullable=False)    # human-readable

    created_at = Column(DateTime(timezone=True), server_default=func.now())
