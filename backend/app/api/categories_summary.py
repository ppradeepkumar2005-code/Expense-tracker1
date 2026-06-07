from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, Category, Expense, Income
from app.schemas.schemas import CategoryCreate, CategoryOut, SummaryOut
from sqlalchemy import func

# ── Categories ──────────────────────────────────────────────
categories_router = APIRouter(prefix="/categories", tags=["Categories"])

DEFAULT_CATEGORIES = ["Food", "Transport", "Bills", "Health", "Shopping", "Entertainment", "Other"]


@categories_router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Seed defaults if not present
    for name in DEFAULT_CATEGORIES:
        if not db.query(Category).filter(Category.name == name, Category.user_id == None).first():
            db.add(Category(name=name, user_id=None))
    db.commit()
    # Return defaults + user's custom categories
    return db.query(Category).filter(
        (Category.user_id == None) | (Category.user_id == user.id)
    ).all()


@categories_router.post("/", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cat = Category(name=data.name, user_id=user.id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


# ── Summary ──────────────────────────────────────────────────
summary_router = APIRouter(prefix="/summary", tags=["Summary"])


@summary_router.get("/", response_model=SummaryOut)
def get_summary(month: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """month format: YYYY-MM  e.g. 2024-04"""
    year, mon = map(int, month.split("-"))

    total_expenses = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user.id,
        func.strftime("%Y", Expense.date) == str(year),
        func.strftime("%m", Expense.date) == f"{mon:02d}"
    ).scalar() or 0.0

    total_income = db.query(func.sum(Income.amount)).filter(
        Income.user_id == user.id,
        func.strftime("%Y", Income.date) == str(year),
        func.strftime("%m", Income.date) == f"{mon:02d}"
    ).scalar() or 0.0

    return SummaryOut(
        month=month,
        total_income=round(total_income, 2),
        total_expenses=round(total_expenses, 2),
        net_balance=round(total_income - total_expenses, 2)
    )
