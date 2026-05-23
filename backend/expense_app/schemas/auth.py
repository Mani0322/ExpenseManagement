from pydantic import BaseModel
from pydantic import EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordSchema(BaseModel):
    email : EmailStr

class ResetPasswordSchema(BaseModel):
    token : str
    new_password :str