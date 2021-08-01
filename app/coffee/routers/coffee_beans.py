
from typing import (
    List
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db


router = APIRouter(
    tags=["coffee-beans"],
    responses={404: {"description": "Not found"}},
)


@router.post("/coffee-beans/", response_model=schemas.CoffeeBean)
async def create_coffee_bean(coffee_bean: schemas.CoffeeBeanCreate, db: Session = Depends(get_db)):

    db_coffee_beans = crud.get_coffee_beans_by_variety(db, variety=coffee_bean.variety)
    
    for db_coffee_bean in db_coffee_beans:
        if (db_coffee_bean.variety == coffee_bean.variety
            and db_coffee_bean.origin == coffee_bean.origin
            and db_coffee_bean.processing == coffee_bean.processing
            and db_coffee_bean.roasting == coffee_bean.roasting
        ):
            return db_coffee_bean
    db_coffee_bean = crud.create_coffee_bean(db, coffee_bean)
    return db_coffee_bean


@router.get("/coffee-beans/{variety}", response_model=List[schemas.CoffeeBean])
async def read_coffee_beans_by_variety(variety: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coffee_beans = crud.get_coffee_beans_by_variety(db, variety, skip=skip, limit=limit)
    return coffee_beans


@router.get("/coffee-beans/{origin}", response_model=List[schemas.CoffeeBean])
async def read_coffee_beans_by_origin(origin: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coffee_beans = crud.get_coffee_beans_by_origin(db, origin, skip=skip, limit=limit)
    return coffee_beans

