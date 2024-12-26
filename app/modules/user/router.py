from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.config.database.database import get_db
from app.models.users import User
from app.modules.user.schema import UserResponse, UserCreate
from app.modules.user.utils import hash_password

router = APIRouter()


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create user",
             response_description="User created")
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user_create.name,
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/list", response_model=List[UserResponse], summary="List users", response_description="List of users")
def get_list_of_users(db: Session = Depends(get_db)):
    return db.query(User).all()
