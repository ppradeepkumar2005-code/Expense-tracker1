from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.models import User, Income

from app.schemas.schemas import (
    IncomeCreate,
    IncomeUpdate,
    IncomeOut
)

from app.core.auth import get_current_user


# No prefix here
router = APIRouter(tags=["Income"])


@router.post("/", response_model=IncomeOut, status_code=201)
def create_income(
    data: IncomeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    income = Income(
        **data.dict(),
        user_id=user.id
    )

    db.add(income)
    db.commit()
    db.refresh(income)

    return income


@router.get("/", response_model=list[IncomeOut])
def list_income(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return (
        db.query(Income)
        .filter(Income.user_id == user.id)
        .order_by(Income.date.desc())
        .all()
    )


@router.put("/{income_id}", response_model=IncomeOut)
def update_income(
    income_id: int,
    data: IncomeUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    income = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == user.id
    ).first()

    if not income:
        raise HTTPException(
            status_code=404,
            detail="Income not found"
        )

    for field, value in data.dict(exclude_unset=True).items():
        setattr(income, field, value)

    db.commit()
    db.refresh(income)

    return income


@router.delete("/{income_id}", status_code=204)
def delete_income(
    income_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    income = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == user.id
    ).first()

    if not income:
        raise HTTPException(
            status_code=404,
            detail="Income not found"
        )

    db.delete(income)
    db.commit()

    return None