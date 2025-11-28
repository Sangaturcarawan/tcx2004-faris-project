# app/members/router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.utils import get_current_user
from app.groups.models import Group
from app.auth.models import User
from app.members.models import GroupMember
from app.schemas import (
    GroupMemberCreate, 
    GroupMemberUpdate, 
    GroupMemberOut)

router = APIRouter(
    prefix="/groups/{group_id}/members",
    tags=["Group Members"],
)

def _get_group_or_404(
        db: Session,
        group_id: int):
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return group

def _get_member_or_404(db: Session, group_id: int, member_id: int):
    member = (
        db.query(GroupMember)
        .filter(
            GroupMember.id == member_id,
            GroupMember.group_id == group_id
        )
        .first()
    )

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


def _ensure_admin(group: Group, user):
    if group.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the group admin (creator) can manage members"
        )

@router.post("/", response_model=GroupMemberOut)
def add_member(
    group_id: int,
    member_in: GroupMemberCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)):

    group = _get_group_or_404(db, group_id)
    _ensure_admin(group, user)

    #check target user exists
    target_user = db.query(User).filter(User.id == member_in.user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=404, 
            detail="User not found")
    
    #check if target user is a member of expense group
    existing = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == member_in.user_id
        ).first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already in group")
    
    member = GroupMember(
        group_id=group_id,
        user_id=member_in.user_id,
        role=member_in.role or "member"
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/", response_model=list[GroupMemberOut])
def list_members(
    group_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)):

    group = _get_group_or_404(db, group_id)

    membership = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user.id
        ).first()
    )

    if not membership and group.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this group"
        )
    
    members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).all()

    return members

@router.put("/{member_id}", response_model=GroupMemberOut)
def update_member(
    group_id: int,
    member_id: int,
    member_in: GroupMemberUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    group = _get_group_or_404(db, group_id)
    _ensure_admin(group, user)

    member = _get_member_or_404(db, group_id, member_id)
    
    member.role = member_in.role
    db.commit()
    db.refresh(member)
    return member

@router.delete("/{member_id}")
def remove_member(
    group_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    group = _get_group_or_404(db, group_id)
    _ensure_admin(group, user)

    member = _get_member_or_404(db, group_id, member_id)

    db.delete(member)
    db.commit()
    return {"message": "Member removed"}