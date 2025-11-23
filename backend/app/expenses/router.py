# app/expenses/router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.utils import get_current_user
from app.groups.models import Group
from app.expenses.models import Expense
from app.schemas import ExpenseCreate, ExpenseOut

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def user_owns_group(db, user, group_id):
    group = db.query(Group).filter(
        Group.id == group_id,
        Group.owner_id == user.id
    ).first()
    return group


@router.post("/group/{group_id}", response_model=ExpenseOut)
def create_expense(
    group_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # Check user owns this group
    if not user_owns_group(db, user, group_id):
        raise HTTPException(status_code=403, detail="Not your group")

    new_expense = Expense(
        amount=expense.amount,
        description=expense.description,
        user_id=user.id,
        group_id=group_id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/group/{group_id}", response_model=list[ExpenseOut])
def list_expenses(
    group_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # Check user owns this group
    if not user_owns_group(db, user, group_id):
        raise HTTPException(status_code=403, detail="Not your group")

    return db.query(Expense).filter(Expense.group_id == group_id).all()
