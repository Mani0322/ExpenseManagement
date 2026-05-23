from sqlalchemy import Column, Integer, String
from sqlalchemy import Float, ForeignKey
from sqlalchemy import DateTime, Text

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from expense_app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    amount = Column(Float, nullable=False)

    notes = Column(Text, nullable=True)

    expense_date = Column(DateTime(timezone=True))

    category_id = Column(Integer, ForeignKey("categories.id"))

    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category")

    user = relationship("User")