from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from expense_app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")