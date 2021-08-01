from typing import List

from fastapi import Depends, FastAPI

from . import models, config, database
from .dependencies import get_settings
from .routers import users, coffee_beans

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(openapi_url="/api/v1/openapi.json")

app.include_router(users.router)
app.include_router(coffee_beans.router)

@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "sqlalchemy_uri": settings.sqlalchemy_uri,
    }

