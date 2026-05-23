from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from fastapi import HTTPException
from expense_app.dependencies.db import get_db

from expense_app.models.user import User

from expense_app.schemas.user import UserCreate
from expense_app.schemas.user import UserResponse
from expense_app.schemas.auth import (
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema
)
from expense_app.schemas.token import RefreshTokenSchema
from expense_app.dependencies.auth import get_current_user
from expense_app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    create_reset_token
)
from expense_app.utils.security import (
    hash_password,
    verify_password,
)




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


@router.post("/login")
def login_user(
    payload : LoginSchema,
    db: Session = Depends(get_db)

):
    user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if not user:
        raise HTTPException(
            status_code = 400,
            detail = "invalid email or password"
        )
    is_valid_password = verify_password(
        payload.password,
        user.password
    )

    if not is_valid_password:
        raise HTTPException(
            status_code = 400,
            detail = "invalid email or password"

        )
    
    access_token = create_access_token(
        data ={
            "user_id":user.id,
            "email":user.email

        }
    )

    refresh_token = create_refresh_token(
        data = {
            "user_id":user.id,
            "email":user.email
        }
    )

    
    return {
        "message":"login successfull",
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer",
    }

@router.post("/refresh-token")
def refresh_access_token(
    payload: RefreshTokenSchema
):

    payload_data = verify_token(
        payload.refresh_token
    )

    if not payload_data:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if payload_data.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    new_access_token = create_access_token(
        data={
            "user_id": payload_data["user_id"]
        }
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.get("/profile",response_model=UserResponse)
def get_profile(
    current_user:User = Depends(get_current_user)
):
    return current_user

@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordSchema,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    reset_token = create_reset_token(
        data={
            "user_id": user.id
        }
    )

    return {
        "message": "Password reset token generated",
        "reset_token": reset_token
    }

@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordSchema,
    db: Session = Depends(get_db)
):

    token_data = verify_token(
        payload.token
    )

    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if token_data.get("type") != "reset":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    user = db.query(User).filter(
        User.id == token_data["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = hash_password(
        payload.new_password
    )

    db.commit()

    return {
        "message": "Password reset successful"
    }