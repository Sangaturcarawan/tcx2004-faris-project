# app/groups/router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.utils import get_current_user
from app.groups.models import Group
from app.schemas import GroupCreate, GroupOut
from app.members.models import GroupMember


router = APIRouter(prefix="/groups", tags=["Groups"])

# Create a new group
@router.post("/", response_model=GroupOut)
def create_group(
    group: GroupCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    new_group = Group(
        name=group.name,
        owner_id=user.id
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    return new_group


# Get all groups belonging to the logged-in user
@router.get("/", response_model=list[GroupOut])
def get_groups(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    groups = db.query(Group).filter(Group.owner_id == user.id).all()
    return groups


# Get one group by ID
@router.get("/{group_id}", response_model=GroupOut)
def get_group(
    group_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    group = db.query(Group).filter(
        Group.id == group_id,
        Group.owner_id == user.id
    ).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return group

@router.put("/{group_id}")
def update_group(
    group_id: int,
    data: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)):

    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    if "name" in data:
        group.name = data["name"]

    db.commit()
    db.refresh(group)

    return group

@router.delete("/{group_id}")
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    db.delete(group)
    db.commit()

    return {"message": "Group deleted"}