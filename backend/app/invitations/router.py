# app/invitations/router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.utils import get_current_user
from app.groups.models import Group
from app.members.models import GroupMember
from app.auth.models import User
from app.invitations.models import GroupInvitation
from app.invitations.schemas import InvitationCreate, InvitationOut

router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"]
)


def _get_group_or_404(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.post("/groups/{group_id}/invite", response_model=InvitationOut)
def send_invite(
    group_id: int,
    invite_in: InvitationCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    group = _get_group_or_404(db, group_id)

    # --- Ensure inviter is a group member ---
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user.id
    ).first()

    if not membership and group.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You are not a member")

    # --- Find invitee ---
    invitee = db.query(User).filter(User.email == invite_in.email).first()
    if not invitee:
        raise HTTPException(status_code=404, detail="No user with that email")

    # Cannot invite yourself
    if invitee.id == user.id:
        raise HTTPException(status_code=400, detail="Cannot invite yourself")

    # Already a group member?
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == invitee.id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this group"
        )

    # Pending invitation already exists?
    pending = db.query(GroupInvitation).filter(
        GroupInvitation.group_id == group_id,
        GroupInvitation.invitee_id == invitee.id,
        GroupInvitation.status == "pending"
    ).first()

    if pending:
        raise HTTPException(
            status_code=400,
            detail="An invitation is already pending"
        )

    # Create the invitation
    invitation = GroupInvitation(
        group_id=group_id,
        inviter_id=user.id,
        invitee_id=invitee.id
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return invitation


@router.get("/received", response_model=list[InvitationOut])
def get_my_invitations(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    invites = db.query(GroupInvitation).filter(
        GroupInvitation.invitee_id == user.id
    ).all()

    return invites


@router.post("/{invitation_id}/accept")
def accept_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    invite = db.query(GroupInvitation).filter(
        GroupInvitation.id == invitation_id,
        GroupInvitation.invitee_id == user.id
    ).first()

    if not invite:
        raise HTTPException(status_code=404, detail="Invitation not found")

    if invite.status != "pending":
        raise HTTPException(status_code=400, detail="Invitation is not pending")

    # Mark accepted
    invite.status = "accepted"

    # Add user as group member
    membership = GroupMember(
        group_id=invite.group_id,
        user_id=user.id,
        role="member"
    )
    db.add(membership)
    db.commit()

    return {"message": "Invitation accepted and membership added"}


@router.post("/{invitation_id}/decline")
def decline_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    invite = db.query(GroupInvitation).filter(
        GroupInvitation.id == invitation_id,
        GroupInvitation.invitee_id == user.id
    ).first()

    if not invite:
        raise HTTPException(status_code=404, detail="Invitation not found")

    invite.status = "declined"
    db.commit()

    return {"message": "Invitation declined"}