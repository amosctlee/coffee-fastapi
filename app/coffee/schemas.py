
from typing import List, Optional
import datetime
from pydantic import BaseModel


class BrewingBase(BaseModel):
    brewed_at: datetime.datetime  # 預設值不能給 function
    equipments: str
    flavor: Optional[str]
    

class BrewingCreate(BrewingBase):
    brewer_id: int
    coffee_bean_id: int


class Brewing(BrewingBase):
    id: int
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    brewings: List[Brewing] = []

    class Config:
        orm_mode = True


class UserOut(UserBase):
    # 列出全部users 時，不要把他們的沖煮紀錄回傳
    is_active: bool
    brewing_count: int

    class Config:
        orm_mode = True



class CoffeeBeanBase(BaseModel):
    variety: str
    origin: str
    processing: str
    roasting: str


class CoffeeBeanCreate(CoffeeBeanBase):
    pass


class CoffeeBean(CoffeeBeanBase):
    id: int
    brewings: List[Brewing] = []

    class Config:
        orm_mode = True

