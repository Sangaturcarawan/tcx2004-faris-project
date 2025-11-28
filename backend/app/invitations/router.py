from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets

from app.deps import get_db
from app.auth.utils import get_current_user
from app.auth.models import User
from app.groups.models import Group
from app.members.models import GroupMember
from app.invitations.models import GroupInvitation
from app.invitations.schemas import InvitationCreate, InvitationOut

router = APIRouter(
    prefix="/groups/{group_id}/invitations",
    tags=["Invitations"]
)

#helper functions
def _get_group(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

def _ensure_admin(group, user):
    if group.owner_id != user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not allowed (admin only)")
    
@router.post("/", response_model=InvitationOut)
def send_invitation(
    group_id: int,
    invite: InvitationCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    group = _get_group(db, group_id)
    _ensure_admin(group, user)

    target = db.query(User).filter(User.email == invite.email).first()
    if not target:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    #check if member already
    existing_member = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id,
                GroupMember.user_id == target.id)
                .first()
    )
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User already in group"
        )
    
    #check pending invites
    existing_inv = (
        db.query(GroupInvitation)
        .filter(GroupInvitation.group_id == group_id,
                GroupInvitation.email == invite.email,
                GroupInvitation.status == "pending")
                .first()
    )
    if existing_inv:
        raise HTTPException(status_code=400, detail="Invitation already")
    
    #create invitation
    token = secrets.token_hex(16)

    inv = GroupInvitation(
        group_id=group_id,
        email=invite.email,
        token=token,
        status="pending"
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)

    return inv