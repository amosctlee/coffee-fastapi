
from typing import Optional
from functools import lru_cache

from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from pydantic import BaseModel

from fastapi import Depends, HTTPException, status

from . import config
from . import schemas, crud


# 每次呼叫都回傳相同value，不用重新讀檔
@lru_cache()
def get_settings():
    # 把settings 放在 dependency 中，可以很方便覆寫 value，測試時尤其有用
    # 以下為覆寫 dependency 的方式
    # def get_settings_override():
    #     return Settings(admin_email="testing_admin@example.com")
    # app.dependency_overrides[get_settings] = get_settings_override

    return config.Settings()



# Dependency
def get_db():
    # 會 return generator，因此直接呼叫回傳的不是 db
    # 最好透過 Depends 來使用
    from .database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_in_db(db, username: str):
    user = crud.get_user_by_username(db, username)
    if user is not None:
        return schemas.UserInDB.from_orm(user)

def authenticate_user(db, username: str, password: str):
    user = get_user_in_db(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_in_db(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.UserInDB = Depends(get_current_user)):
    if current_user.is_active is not True:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

