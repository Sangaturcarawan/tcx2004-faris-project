# app/expenses/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)

    # NEW FIELDS REQUIRED FOR USER STORY 6
    date = Column(DateTime, default=datetime.utcnow)
    shares = Column(Text, nullable=True)  # JSON string storing cost breakdown

    created_at = Column(DateTime, default=datetime.utcnow)

    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    payer = relationship("User")
    group = relationship("Group")




# from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.database import Base


# class Expense(Base):
#     __tablename__ = "expenses"

#     id = Column(Integer, primary_key=True, index=True)
#     amount = Column(Float, nullable=False)
#     description = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     user_id = Column(Integer, ForeignKey("users.id"))
#     group_id = Column(Integer, ForeignKey("groups.id"))

#     user = relationship("User")
#     group = relationship("Group")
