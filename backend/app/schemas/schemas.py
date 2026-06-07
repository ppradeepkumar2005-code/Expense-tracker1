from pydantic import BaseModel
from datetime import date
from typing import Optional


# ---------------- USER SCHEMAS ----------------
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


# ---------------- EXPENSE SCHEMAS ----------------
class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: date
    note: Optional[str] = None

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[date] = None
    note: Optional[str] = None

class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    date: date
    note: Optional[str]
    user_id: int
    class Config:
        from_attributes = True


# ---------------- INCOME SCHEMAS ----------------
class IncomeCreate(BaseModel):
    amount: float
    source: str
    date: date

class IncomeUpdate(BaseModel):
    amount: Optional[float] = None
    source: Optional[str] = None
    date: Optional[date] = None

class IncomeOut(BaseModel):
    id: int
    amount: float
    source: str
    date: date
    user_id: int
    class Config:
        from_attributes = True


# ---------------- CATEGORY SCHEMAS ----------------
class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True


# ---------------- SUMMARY SCHEMA ----------------
class SummaryOut(BaseModel):
    month: str
    total_income: float
    total_expenses: float
    net_balance: float
