import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.config.jwt.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return {
        "token": jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM),
        "expires_in": expire,
    }


def create_refresh_token():
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return {
        "token": jwt.encode({"exp": expire}, SECRET_KEY, algorithm=ALGORITHM),
        "expires_at": expire,
    }


def verify_token(token: str):
    username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print('username', username)
    return username


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
