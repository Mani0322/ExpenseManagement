from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from expense_app.database import Base, engine
from expense_app.models.user import User
from expense_app.models.category import Category
from expense_app.models.expense import Expense
from expense_app.routes.auth import router as auth_router
from expense_app.routes.category import router as category_router
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Expense Management API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(auth_router)
app.include_router(category_router)
@app.get("/")
def home():
    return {"message":"Running Backend"}

