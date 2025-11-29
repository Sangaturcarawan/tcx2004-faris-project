# print(">>> LOADED EXPENSE ROUTER FROM THIS FILE <<<")

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime
# import json

# from app.deps import get_db
# from app.auth.utils import get_current_user
# from app.groups.models import Group
# from app.members.models import GroupMember
# from app.expenses.models import Expense
# from app.schemas import ExpenseCreate, ExpenseOut
# from app.audit.utils import create_audit_log

# router = APIRouter(prefix="/expenses", tags=["Expenses"])


# def is_group_member(db, user_id, group_id):
#     return db.query(GroupMember).filter(
#         GroupMember.group_id == group_id,
#         GroupMember.user_id == user_id
#     ).first()


# def get_group_or_404(db: Session, group_id: int):
#     group = db.query(Group).filter(Group.id == group_id).first()
#     if not group:
#         raise HTTPException(404, "Group not found")
#     return group


# # -------------------------------------------------------
# # CREATE EXPENSE
# # -------------------------------------------------------

# @router.post("/group/{group_id}", response_model=ExpenseOut)
# def create_expense(
#     group_id: int,
#     expense: ExpenseCreate,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     group = get_group_or_404(db, group_id)

#     if not is_group_member(db, user.id, group_id) and group.owner_id != user.id:
#         raise HTTPException(403, "You are not a member of this group")

#     shares_json = json.dumps(expense.shares) if expense.shares else None

#     new_expense = Expense(
#         amount=expense.amount,
#         description=expense.description,
#         date=expense.date or datetime.utcnow(),
#         shares=shares_json,
#         payer_id=user.id,
#         group_id=group_id
#     )

#     db.add(new_expense)
#     db.commit()
#     db.refresh(new_expense)

#     create_audit_log(
#         db=db,
#         group_id=group_id,
#         user_id=user.id,
#         action="expense_created",
#         description=f"{user.email} created an expense of ${expense.amount}."
#     )

#     return ExpenseOut(
#         id=new_expense.id,
#         amount=new_expense.amount,
#         description=new_expense.description,
#         date=new_expense.date,
#         payer_id=new_expense.payer_id,
#         group_id=new_expense.group_id,
#         shares=json.loads(new_expense.shares) if new_expense.shares else None
#     )


# # -------------------------------------------------------
# # LIST EXPENSES
# # -------------------------------------------------------

# @router.get("/group/{group_id}", response_model=list[ExpenseOut])
# def list_expenses(
#     group_id: int,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     group = get_group_or_404(db, group_id)

#     if not is_group_member(db, user.id, group_id) and group.owner_id != user.id:
#         raise HTTPException(403, "You are not a member of this group")

#     expenses = db.query(Expense).filter(Expense.group_id == group_id).all()

#     result = []
#     for exp in expenses:
#         result.append(
#             ExpenseOut(
#                 id=exp.id,
#                 amount=exp.amount,
#                 description=exp.description,
#                 date=exp.date,
#                 payer_id=exp.payer_id,
#                 group_id=exp.group_id,
#                 shares=json.loads(exp.shares) if exp.shares else None
#             )
#         )

#     return result


# # -------------------------------------------------------
# # UPDATE EXPENSE
# # -------------------------------------------------------

# @router.put("/{expense_id}", response_model=ExpenseOut)
# def update_expense(
#     expense_id: int,
#     expense_data: ExpenseCreate,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     exp = db.query(Expense).filter(Expense.id == expense_id).first()
#     if not exp:
#         raise HTTPException(404, "Expense not found")

#     group = get_group_or_404(db, exp.group_id)

#     if group.owner_id != user.id and exp.payer_id != user.id:
#         raise HTTPException(403, "You can only update expenses you created")

#     exp.amount = expense_data.amount
#     exp.description = expense_data.description
#     exp.date = expense_data.date or exp.date
#     exp.shares = json.dumps(expense_data.shares) if expense_data.shares else exp.shares

#     db.commit()
#     db.refresh(exp)

#     create_audit_log(
#         db=db,
#         group_id=exp.group_id,
#         user_id=user.id,
#         action="expense_updated",
#         description=f"{user.email} updated expense #{expense_id}."
#     )

#     return ExpenseOut(
#         id=exp.id,
#         amount=exp.amount,
#         description=exp.description,
#         date=exp.date,
#         payer_id=exp.payer_id,
#         group_id=exp.group_id,
#         shares=json.loads(exp.shares) if exp.shares else None
#     )


# # -------------------------------------------------------
# # DELETE EXPENSE
# # -------------------------------------------------------

# @router.delete("/{expense_id}")
# def delete_expense(
#     expense_id: int,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     exp = db.query(Expense).filter(Expense.id == expense_id).first()
#     if not exp:
#         raise HTTPException(404, "Expense not found")

#     group = get_group_or_404(db, exp.group_id)

#     if group.owner_id != user.id and exp.payer_id != user.id:
#         raise HTTPException(403, "You can only delete expenses you created")

#     db.delete(exp)
#     db.commit()

#     create_audit_log(
#         db=db,
#         group_id=exp.group_id,
#         user_id=user.id,
#         action="expense_deleted",
#         description=f"{user.email} deleted expense #{expense_id}."
#     )

#     return {"message": "Expense deleted"}




# print(">>> LOADED EXPENSE ROUTER FROM THIS FILE <<<")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.deps import get_db
from app.auth.utils import get_current_user
from app.groups.models import Group
from app.members.models import GroupMember
from app.expenses.models import Expense
from app.schemas import ExpenseCreate, ExpenseOut
from app.audit.utils import create_audit_log

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# -------------------------------------------------------
# Helper functions
# -------------------------------------------------------

def is_group_member(db, user_id, group_id):
    return db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()


def get_group_or_404(db: Session, group_id: int):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(404, "Group not found")
    return group


# -------------------------------------------------------
# CREATE EXPENSE
# -------------------------------------------------------

@router.post("/group/{group_id}", response_model=ExpenseOut)
def create_expense(
    group_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Create a new expense inside a group."""
    group = get_group_or_404(db, group_id)

    if not is_group_member(db, user.id, group_id) and group.owner_id != user.id:
        raise HTTPException(403, "You are not a member of this group")

    new_expense = Expense(
        amount=expense.amount,
        description=expense.description,
        date=expense.date or datetime.utcnow(),
        shares=json.dumps(expense.shares) if expense.shares else None,
        payer_id=user.id,
        group_id=group_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    # Ensure shares become a dict when returning
    if new_expense.shares:
        new_expense.shares = json.loads(new_expense.shares)

    create_audit_log(
        db=db,
        group_id=group_id,
        user_id=user.id,
        action="expense_created",
        description=f"{user.email} created an expense of ${expense.amount}."
    )

    return new_expense


# -------------------------------------------------------
# LIST EXPENSES
# -------------------------------------------------------

@router.get("/group/{group_id}", response_model=list[ExpenseOut])
def list_expenses(
    group_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    group = get_group_or_404(db, group_id)

    if not is_group_member(db, user.id, group_id) and group.owner_id != user.id:
        raise HTTPException(403, "You are not a member of this group")

    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()

    for exp in expenses:
        if exp.shares:
            exp.shares = json.loads(exp.shares)

    return expenses


# -------------------------------------------------------
# UPDATE EXPENSE
# -------------------------------------------------------

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    exp = db.query(Expense).filter(Expense.id == expense_id).first()
    if not exp:
        raise HTTPException(404, "Expense not found")

    group = get_group_or_404(db, exp.group_id)

    # Admin can edit anything, members can ONLY edit what they created
    if group.owner_id != user.id and exp.payer_id != user.id:
        raise HTTPException(403, "You can only update expenses you created")

    exp.amount = expense_data.amount
    exp.description = expense_data.description
    exp.date = expense_data.date or exp.date
    exp.shares = json.dumps(expense_data.shares) if expense_data.shares else exp.shares

    db.commit()
    db.refresh(exp)

    create_audit_log(
        db=db,
        group_id=exp.group_id,
        user_id=user.id,
        action="expense_updated",
        description=f"{user.email} updated expense #{expense_id}."
    )

    if exp.shares:
        exp.shares = json.loads(exp.shares)

    return exp


# -------------------------------------------------------
# DELETE EXPENSE
# -------------------------------------------------------

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    exp = db.query(Expense).filter(Expense.id == expense_id).first()
    if not exp:
        raise HTTPException(404, "Expense not found")

    group = get_group_or_404(db, exp.group_id)

    # Admin can delete anything, members can ONLY delete their own
    if group.owner_id != user.id and exp.payer_id != user.id:
        raise HTTPException(403, "You can only delete expenses you created")

    db.delete(exp)
    db.commit()

    create_audit_log(
        db=db,
        group_id=exp.group_id,
        user_id=user.id,
        action="expense_deleted",
        description=f"{user.email} deleted expense #{expense_id}."
    )

    return {"message": "Expense deleted"}




# # app/expenses/router.py

# print(">>> LOADED EXPENSE ROUTER FROM THIS FILE <<<")


# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime

# import json

# from app.deps import get_db
# from app.auth.utils import get_current_user
# from app.groups.models import Group
# from app.members.models import GroupMember
# from app.expenses.models import Expense
# from app.schemas import ExpenseCreate, ExpenseOut
# from app.audit.utils import create_audit_log

# router = APIRouter(prefix="/expenses", tags=["Expenses"])


# def is_group_member(db, user_id, group_id):
#     return db.query(GroupMember).filter(
#         GroupMember.group_id == group_id,
#         GroupMember.user_id == user_id
#     ).first()


# def get_group_or_404(db, group_id):
#     group = db.query(Group).filter(Group.id == group_id).first()
#     if not group:
#         raise HTTPException(404, "Group not found")
#     return group



# @router.post("/group/{group_id}", response_model=ExpenseOut)
# def create_expense(
#     group_id: int,
#     expense: ExpenseCreate,
#     db: Session = Depends(get_db),
#     user = Depends(get_current_user)
# ):
#     group = get_group_or_404(db, group_id)

#     if not is_group_member(db, user.id, group_id) and group.owner_id != user.id:
#         raise HTTPException(403, "You are not a member of this group")

#     new_expense = Expense(
#         amount=expense.amount,
#         description=expense.description,
#         date=expense.date or datetime.utcnow()
#         shares=json.dumps(expense.shares) if expense.shares else None,
#         payer_id=user.id,
#         group_id=group_id
#     )

#     db.add(new_expense)
#     db.commit()
#     db.refresh(new_expense)

#     # FIX: convert JSON string → dict
#     if new_expense.shares:
#         new_expense.shares = json.loads(new_expense.shares)

#     create_audit_log(
#         db=db,
#         group_id=group_id,
#         user_id=user.id,
#         action="expense_created",
#         description=f"{user.email} created an expense of ${expense.amount}."
#     )

#     return new_expense



# # -----------------------------
# # LIST EXPENSES (ALL MEMBERS)
# # -----------------------------
# @router.get("/group/{group_id}", response_model=list[ExpenseOut])
# def list_expenses(
#     group_id: int,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):

#     group = get_group_or_404(db, group_id)

#     if not is_group_member(db, user.id, group_id) and group.owner_id != user.id:
#         raise HTTPException(403, "You are not a member of this group")

#     expenses = db.query(Expense).filter(Expense.group_id == group_id).all()

#     # Convert shares JSON → dict
#     for e in expenses:
#         if e.shares:
#             e.shares = json.loads(e.shares)

#     return expenses


# # -----------------------------
# # UPDATE EXPENSE
# # -----------------------------
# @router.put("/{expense_id}", response_model=ExpenseOut)
# def update_expense(
#     expense_id: int,
#     expense_data: ExpenseCreate,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):

#     exp = db.query(Expense).filter(Expense.id == expense_id).first()
#     if not exp:
#         raise HTTPException(404, "Expense not found")

#     group = get_group_or_404(db, exp.group_id)

#     # Admin can edit any expense
#     if group.owner_id != user.id:
#         # Member can edit ONLY their own
#         if exp.payer_id != user.id:
#             raise HTTPException(403, "You can only update expenses you created")

#     exp.amount = expense_data.amount
#     exp.description = expense_data.description
#     exp.date = expense_data.date or exp.date
#     exp.shares = json.dumps(expense_data.shares) if expense_data.shares else exp.shares

#     db.commit()
#     db.refresh(exp)

#     create_audit_log(
#         db=db,
#         group_id=exp.group_id,
#         user_id=user.id,
#         action="expense_updated",
#         description=f"{user.email} updated expense #{expense_id}."
#     )

#     if exp.shares:
#         exp.shares = json.loads(exp.shares)

#     return exp


# # -----------------------------
# # DELETE EXPENSE
# # -----------------------------
# @router.delete("/{expense_id}")
# def delete_expense(
#     expense_id: int,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):

#     exp = db.query(Expense).filter(Expense.id == expense_id).first()
#     if not exp:
#         raise HTTPException(404, "Expense not found")

#     group = get_group_or_404(db, exp.group_id)

#     # Admin can delete any
#     if group.owner_id != user.id:
#         # Members can delete ONLY their own
#         if exp.payer_id != user.id:
#             raise HTTPException(403, "You can only delete expenses you created")

#     db.delete(exp)
#     db.commit()

#     create_audit_log(
#         db=db,
#         group_id=exp.group_id,
#         user_id=user.id,
#         action="expense_deleted",
#         description=f"{user.email} deleted expense #{expense_id}."
#     )

#     return {"message": "Expense deleted"}





# # # app/expenses/router.py

# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.orm import Session

# # from app.deps import get_db
# # from app.auth.utils import get_current_user
# # from app.groups.models import Group
# # from app.expenses.models import Expense
# # from app.schemas import ExpenseCreate, ExpenseOut
# # from app.audit.utils import create_audit_log


# # router = APIRouter(prefix="/expenses", tags=["Expenses"])


# # def user_owns_group(db, user, group_id):
# #     group = db.query(Group).filter(
# #         Group.id == group_id,
# #         Group.owner_id == user.id
# #     ).first()
# #     return group


# # @router.post("/group/{group_id}", response_model=ExpenseOut)
# # def create_expense(
# #     group_id: int,
# #     expense: ExpenseCreate,
# #     db: Session = Depends(get_db),
# #     user = Depends(get_current_user)
# # ):
# #     # Check user owns this group
# #     if not user_owns_group(db, user, group_id):
# #         raise HTTPException(status_code=403, detail="Not your group")

# #     new_expense = Expense(
# #         amount=expense.amount,
# #         description=expense.description,
# #         user_id=user.id,
# #         group_id=group_id
# #     )
# #     db.add(new_expense)
# #     db.commit()
# #     db.refresh(new_expense)

# #     create_audit_log(
# #         db=db,
# #         group_id=group_id,
# #         user_id=user.id,
# #         action="expense_created",
# #         description=f"{user.email} created an expense of ${expense.amount} titled '{expense.description}'."
# #     )

# #     return new_expense




# # @router.get("/group/{group_id}", response_model=list[ExpenseOut])
# # def list_expenses(
# #     group_id: int,
# #     db: Session = Depends(get_db),
# #     user = Depends(get_current_user)
# # ):
# #     # Check user owns this group
# #     if not user_owns_group(db, user, group_id):
# #         raise HTTPException(status_code=403, detail="Not your group")

# #     return db.query(Expense).filter(Expense.group_id == group_id).all()


# # @router.put("/{expense_id}", response_model=ExpenseOut)
# # def update_expense(
# #     expense_id: int,
# #     expense_data: ExpenseCreate,
# #     db: Session = Depends(get_db),
# #     user = Depends(get_current_user)
# # ):
# #     exp = db.query(Expense).filter(
# #         Expense.id == expense_id
# #     ).first()

# #     if not exp:
# #         raise HTTPException(status_code=404, detail="Expense not found")

# #     if not user_owns_group(db, user, exp.group_id):
# #         raise HTTPException(status_code=403, detail="Not your group")

# #     exp.amount = expense_data.amount
# #     exp.description = expense_data.description
# #     db.commit()
# #     db.refresh(exp)

# #     create_audit_log(
# #         db=db,
# #         group_id=exp.group_id,
# #         user_id=user.id,
# #         action="expense_updated",
# #         description=f"{user.email} updated expense #{expense_id}."
# #     )

# #     return exp



# # @router.delete("/{expense_id}")
# # def delete_expense(
# #     expense_id: int,
# #     db: Session = Depends(get_db),
# #     user = Depends(get_current_user)
# # ):
# #     exp = db.query(Expense).filter(
# #         Expense.id == expense_id
# #     ).first()

# #     if not exp:
# #         raise HTTPException(status_code=404, detail="Expense not found")

# #     if not user_owns_group(db, user, exp.group_id):
# #         raise HTTPException(status_code=403, detail="Not your group")

# #     db.delete(exp)
# #     db.commit()

# #     create_audit_log(
# #         db=db,
# #         group_id=exp.group_id,
# #         user_id=user.id,
# #         action="expense_deleted",
# #         description=f"{user.email} deleted expense #{expense_id}."
# #     )

# #     return {"message": "Expense deleted"}

