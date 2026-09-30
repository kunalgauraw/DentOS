import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core import Base, get_db, get_password_hash
from app.models import User, UserRole

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ADMIN = {"username": "testadmin", "password": "testpass123"}
RECEPTIONIST = {"username": "reception", "password": "reception123"}


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    db.add_all([
        User(
            username=ADMIN["username"],
            password_hash=get_password_hash(ADMIN["password"]),
            full_name="Test Admin",
            role=UserRole.ADMIN,
            mobile="9999999999",
        ),
        User(
            username=RECEPTIONIST["username"],
            password_hash=get_password_hash(RECEPTIONIST["password"]),
            full_name="Front Desk",
            role=UserRole.RECEPTIONIST,
            mobile="9999999998",
        ),
    ])
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override"""
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def _login(client, creds):
    response = client.post("/auth/login", json=creds)
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def auth_headers(client):
    """Admin auth headers"""
    return _login(client, ADMIN)


@pytest.fixture
def receptionist_headers(client):
    """Receptionist (non-admin) auth headers"""
    return _login(client, RECEPTIONIST)


@pytest.fixture
def patient(client, auth_headers):
    """A saved patient, returned as the API response dict"""
    response = client.post(
        "/patients/",
        json={"full_name": "Fixture Patient", "mobile": "9000000001", "gender": "female", "age": 28},
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    return response.json()
