# app/payments/router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth.utils import get_current_user
from app.groups.models import Group
from app.expenses.models import Expense

router = APIRouter(prefix="/payments", tags=["Payments"])


# Check user owns the group
def user_owns_group(db, user, group_id):
    return db.query(Group).filter(
        Group.id == group_id,
        Group.owner_id == user.id
    ).first()


@router.get("/group/{group_id}/summary")
def payment_summary(
    group_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # Ownership check
    if not user_owns_group(db, user, group_id):
        raise HTTPException(status_code=403, detail="Not your group")

    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    total_spent = sum(e.amount for e in expenses)

    return {
        "group_id": group_id,
        "total_spent": total_spent,
        "num_expenses": len(expenses),
        "balance": 0,               # simple version ---
        "expenses": expenses
    }
