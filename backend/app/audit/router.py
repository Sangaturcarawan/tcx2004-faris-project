from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.utils import get_current_user
from app.audit.models import AuditLog
from app.audit.schemas import AuditLogOut
from app.groups.models import Group

router = APIRouter(
    prefix="/audit",
    tags=["Audit Logs"]
)

def _ensure_group_admin(group_id: int, user, db):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(404, "Group not found")
    if group.owner_id != user.id:
        raise HTTPException(403, "Only group admin can view audit logs")
    return group


@router.get("/group/{group_id}", response_model=list[AuditLogOut])
def get_group_audit_logs(
    group_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    _ensure_group_admin(group_id, user, db)

    logs = db.query(AuditLog).filter(
        AuditLog.group_id == group_id
    ).order_by(AuditLog.created_at.desc()).all()

    return logs
