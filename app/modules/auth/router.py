from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database.database import get_db
from app.config.jwt.security import create_access_token, create_refresh_token
from app.models.auth import Access
from app.models.users import User
from app.modules.user.utils import verify_password

router = APIRouter()


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    if not email:
        raise HTTPException(status_code=400, detail="Email must be provided")

    user = db.query(User).filter(email == User.email).first()
    checked_pass = verify_password(password, user.hashed_password)
    if not user or not checked_pass:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token()

    access_entry = Access(
        user_id=user.id,
        refresh_token=refresh_token["token"],
        expires_at=refresh_token["expires_at"]
    )
    db.add(access_entry)
    db.commit()

    return {"access_token": access_token["token"], "refresh_token": refresh_token["token"]}


@router.post("/refresh-token")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    token = db.query().filter(refresh_token == Access.refresh_token).first()
    if not token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    print({"token": token})
    user = db.query(User).filter(User.id == token.user_id).first()
    access_token = create_access_token({"sub": user.email})

    return {"access_token": access_token}
