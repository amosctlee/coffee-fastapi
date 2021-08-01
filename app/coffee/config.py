from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "coffee brewing diary"
    sqlalchemy_uri: str = "postgresql://postgres:coffeedb@db:5432/coffeedb"
    SECRET_KEY = "639102d2befd64832b1c8b44872e19b557e605597e35379f2eeed4af8bd527e5"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    # class Config:
    #     env_file = ".env"
