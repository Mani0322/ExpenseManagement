from fastapi import FastAPI
from expense_app.database import Base, engine
from expense_app.models.user import User
from expense_app.models.category import Category
from expense_app.models.expense import Expense

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Expense Management API"
)

@app.get("/")
def home():
    return {"message":"Running Backend"}

