from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from fastapi import HTTPException
from expense_app.dependencies.db import get_db

from expense_app.models.user import User

from expense_app.schemas.user import UserCreate
from expense_app.schemas.user import UserResponse
from expense_app.utils.security import hash_password



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    # Check existing user
    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # hashed password
    hashed_password = hash_password(
        payload.password
    )

    # Create user
    user = User(
        name=payload.name,
        email=payload.email,
        password=hashed_password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user