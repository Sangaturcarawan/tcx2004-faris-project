# backend/app/audit/utils.py

from app.audit.models import AuditLog

def create_audit_log(db, group_id: int, user_id: int, action: str, description: str):
    log = AuditLog(
        group_id=group_id,
        user_id=user_id,
        action_type=action,
        description=description
    )
    db.add(log)
    db.commit()
