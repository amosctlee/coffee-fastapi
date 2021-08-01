
from typing import (
    List
)
from fastapi import HTTPException, APIRouter, Depends

from sqlalchemy.orm import Session
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db=db, user=user)
    
    return db_user



@router.get("/", response_model=List[schemas.UserOut])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    users_out = []
    for user in users:
        users_out.append(schemas.UserOut(
            **schemas.User.from_orm(user).dict(),
                brewing_count=len(user.brewings)
            )
        )
    
    return users_out
    

@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/brewing/{coffee_bean_id}", response_model=schemas.Brewing)
async def create_brewing(
        user_id: int,
        coffee_bean_id: int,
        brewing_base: schemas.BrewingBase, 
        db: Session = Depends(get_db)
    ):
    brewing = schemas.BrewingCreate(**brewing_base.dict(), brewer_id=user_id, coffee_bean_id=coffee_bean_id)
    db_brewing = crud.create_brewing(db, brewing)
    
    return db_brewing


@router.get("/{user_id}/brewings", response_model=List[schemas.Brewing])
async def read_user_brewings(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user.brewings

