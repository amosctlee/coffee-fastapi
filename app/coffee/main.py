from typing import List

from sqlalchemy.ext import declarative
from datetime import timedelta

from sqlalchemy.orm.session import Session
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from . import models, config, database, dependencies
from .routers import users, coffee_beans


# 應該要用 Alembic 來創建資料庫，這邊暫時直接創建
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    openapi_url="/api/v1/openapi.json",
    title="Coffee Brewing Diary API",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "coffee man",
        "url": "http://coffee_man.example.com/contact/",
        "email": "coffee_man@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    )

app.include_router(users.router)
app.include_router(coffee_beans.router)

@app.get("/info")
async def info(settings: config.Settings = Depends(dependencies.get_settings)):
    return {
        "app_name": settings.app_name,
        "sqlalchemy_uri": settings.sqlalchemy_uri,
    }


@app.post("/token", response_model=dependencies.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), 
        settings: config.Settings = Depends(dependencies.get_settings),
        db: Session = Depends(dependencies.get_db)
    ):

    user = dependencies.authenticate_user(
        db, form_data.username, form_data.password)  # 規範是username，實際內容是email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
