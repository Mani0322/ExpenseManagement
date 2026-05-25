from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from expense_app.dependencies.db import get_db
from expense_app.dependencies.auth import get_current_user
from expense_app.schemas.category import CategoryResponse
from expense_app.models.user import User
from expense_app.models.category import Category

router = APIRouter(
   prefix = "/category",
   tags = ["Category"]
)


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    categories = db.query(Category).filter(
        Category.user_id == current_user.id
    ).all()

    return categories