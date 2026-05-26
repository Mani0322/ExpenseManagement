from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from expense_app.dependencies.db import get_db
from expense_app.dependencies.auth import get_current_user
from expense_app.schemas.category import (
    CategoryResponse,
    CategoryUpdate,
)
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

@router.get(
    "/{category_id}",
    response_model = CategoryResponse
)
def get_category(
    category_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code = 404,
            detail = "category not found"
        )
    return category

@router.put(
    "/{category_id}",
    response_model = CategoryResponse
)
def update_category(
    category_id:int,
    payload = CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id

    ).first()

    if not category:
        raise HTTPException(
            status_code = 404,
            detail = 'category not found'
        )
    
    category.name = payload.name
    db.commit()
    db.refresh(category)
    return category
    

@router.delete(
    "/{category_id}"
)
def delete_category(
    category_id : int,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code = 404,
            detail = "category not found"
        )
    db.delete(category)

    db.commit()

    return {
        "message":"Category deleted successfully"
    }