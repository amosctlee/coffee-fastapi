from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String,
    Text, DateTime
)
from sqlalchemy.orm import relationship
import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    brewings = relationship("Brewing", back_populates="brewer")
    

class Brewing(Base):
    __tablename__ = "brewing"

    id = Column(Integer, primary_key=True, index=True)
    brewed_at = Column(DateTime, default=datetime.datetime.now)

    equipments = Column(Text)  # 會有多種，暫時先用文字存
    flavor = Column(Text)

    brewer_id = Column(Integer, ForeignKey("users.id"))
    coffee_bean_id = Column(Integer, ForeignKey("coffee_bean.id"))

    brewer = relationship("User", back_populates="brewings")
    coffee_bean = relationship("CoffeeBean", back_populates="brewings")


class CoffeeBean(Base):
    __tablename__ = "coffee_bean"

    id = Column(Integer, primary_key=True, index=True)
    
    variety = Column(String)  # 品種
    origin = Column(String)  # 產地
    processing = Column(String)  # 處理法
    roasting = Column(String)  # 烘焙度

    brewings = relationship("Brewing", back_populates="coffee_bean")
