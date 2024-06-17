# tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base, User
import schemas

# Setup the database URL for testing (use a separate test database)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create an engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_db():
    # Setup
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown
    Base.metadata.drop_all(bind=engine)

def test_add_user(setup_db):
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123"
    }

    response = client.post("/users", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert "id" in data
    
    # Check if user was added to the database
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "john.doe@example.com").first()
    assert user is not None
    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"
    db.close()
