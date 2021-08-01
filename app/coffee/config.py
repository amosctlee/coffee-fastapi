from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "coffee brewing diary"
    sqlalchemy_uri: str = "postgresql://postgres:coffeedb@db:5432/coffeedb"

    # class Config:
    #     env_file = ".env"
