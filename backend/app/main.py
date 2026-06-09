from fastapi import FastAPI

from app.core.database import Base, engine

from app.api.auth import router as auth_router
from app.api.expenses import router as expenses_router
from app.api.income import router as income_router
from app.api.categories_summary import (
    categories_router,
    summary_router
)

# ---------------- CREATE TABLES ----------------

Base.metadata.create_all(bind=engine)

# ---------------- APP INIT ----------------

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)

# ---------------- ROUTERS ----------------

app.include_router(auth_router)

app.include_router(
    expenses_router,
    prefix="/expenses",
    tags=["Expenses"]
)

app.include_router(
    income_router,
    prefix="/income",
    tags=["Income"]
)

app.include_router(
    categories_router,
    prefix="/categories",
    tags=["Categories"]
)

app.include_router(
    summary_router,
    prefix="/summary",
    tags=["Summary"]
)

# ---------------- HEALTH CHECK ----------------

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------- ROOT ----------------

@app.get("/")
def root():
    return {
        "message": "Expense Tracker API is running 🚀"
    }