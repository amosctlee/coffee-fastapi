from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, 
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_coffee_beans_by_variety(db: Session, variety: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.CoffeeBean)
        .filter(models.CoffeeBean.variety == variety)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_coffee_beans_by_origin(db: Session, origin: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.CoffeeBean)
        .filter(models.CoffeeBean.origin == origin)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_coffee_bean(db: Session, coffee_bean: schemas.CoffeeBeanCreate):
    db_coffee_bean = models.CoffeeBean(**coffee_bean.dict())
    db.add(db_coffee_bean)
    db.commit()
    db.refresh(db_coffee_bean)
    return db_coffee_bean


def create_brewing(db: Session, brewing: schemas.BrewingCreate):
    db_brewing = models.Brewing(**brewing.dict())
    db.add(db_brewing)
    db.commit()
    db.refresh(db_brewing)
    return db_brewing

