from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.core.database import get_db

from app.models.models import User, Expense

from app.schemas.schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseOut
)

from app.core.auth import get_current_user


# No prefix here
router = APIRouter(tags=["Expenses"])


@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    expense = Expense(
        **data.dict(),
        user_id=user.id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.get("/", response_model=list[ExpenseOut])
def list_expenses(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Expense).filter(
        Expense.user_id == user.id
    )

    if start_date:
        query = query.filter(
            Expense.date >= start_date
        )

    if end_date:
        query = query.filter(
            Expense.date <= end_date
        )

    if category:
        query = query.filter(
            Expense.category == category
        )

    return query.order_by(
        Expense.date.desc()
    ).all()


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    for field, value in data.dict(exclude_unset=True).items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


@router.delete("/{expense_id}", status_code=204)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return None