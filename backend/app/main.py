# app/main.py

from fastapi import FastAPI, Depends
from app.database import Base, engine
from app.auth.utils import get_current_user
from app.members.models import GroupMember

from app.auth.router import router as auth_router
from app.groups.router import router as groups_router
from app.expenses.router import router as expenses_router
from app.payments.router import router as payments_router
from app.members.router import router as members_router




# Create FastAPI application instance
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth_router)
app.include_router(groups_router)
app.include_router(expenses_router)
app.include_router(payments_router)
app.include_router(members_router)


@app.get("/")
def home():
    return {"message": "Backend running!"}

@app.get("/me")
def me(user = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}
