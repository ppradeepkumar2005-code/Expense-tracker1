from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import hash_password, verify_password, create_access_token
from app.models.models import User
from app.schemas.schemas import UserCreate, UserOut, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.username == data.username).first()

        if existing:
            return {"message": "Username already taken"}

        user = User(
            username=data.username,
            password=hash_password(data.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "Registered Successfully",
            "id": user.id
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
