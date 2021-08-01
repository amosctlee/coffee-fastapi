import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database


from ..config import Settings
from ..main import app, dependencies, models


# 如果db uri 不在config.py 裡面時，可以在這邊覆寫
# # https://fastapi.tiangolo.com/advanced/testing-database/
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:coffeedb@db/testing"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[dependencies.get_db] = override_get_db


def override_get_settings():
    return Settings(sqlalchemy_uri=SQLALCHEMY_DATABASE_URL)

app.dependency_overrides[dependencies.get_settings] = override_get_settings


client = TestClient(app)


def test_info():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "coffee brewing diary",
        "sqlalchemy_uri": "postgresql://postgres:coffeedb@db/testing",
    }

# https://github.com/tiangolo/fastapi/issues/831
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    try:
        assert not database_exists(SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."
        create_database(SQLALCHEMY_DATABASE_URL)  # Create the test database.
        models.Base.metadata.create_all(bind=engine)  # Create the tables.
        yield  # Run the tests.
    finally:
        drop_database(SQLALCHEMY_DATABASE_URL)  # Drop the test database.



def test_create_user():
    new_user = {
    "username": "testttt",
    "email": "testttt@test.com",
    "password": "123456"
    }
    
    response = client.post("/users", json=new_user, allow_redirects=True)
    data = response.json()

    assert response.status_code == 201
    assert data == {
        "username": "testttt",
        "email": "testttt@test.com",
        "id": 1,
        "is_active": True,
        "brewings": []
    }


def test_read_users():
    pass

def test_read_user():
    pass

def test_create_brewing():
    pass

def test_read_user_brewings():
    pass

def test_create_coffee_bean():
    pass

def test_read_coffee_beans_by_variety():
    pass

def test_read_coffee_beans_by_origin():
    pass
