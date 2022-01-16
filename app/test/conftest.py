from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.token import create_access_token, verify_access_token

from ..main import app
from ..db.connection import connect_db, Base
from ..settings import env

SQL_TEST_DB_URL = f"postgresql://{env.pg_username}:{env.pg_password}@{env.pg_port}/{env.pg_test_db_name}"

engine = create_engine(SQL_TEST_DB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# DB Connection Fixtures


@pytest.fixture(scope="module", name="session")
def prep_session():
    """Cleans up previous test data and sets up a clean DB for testing"""
    # Clean up DB before tests
    Base.metadata.drop_all(bind=engine)
    # Set up tables
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", name="client")
def setup_client(session):
    """Main DB client setup method for testing"""

    def override_connect_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[connect_db] = override_connect_db
    yield TestClient(app)


# Auth Fixtures


@pytest.fixture(name="t_user")
def test_user(client):
    """Create test user for login endpoint"""
    user_input = {"username": "tester0", "password": "testing"}
    res = client.post("users/new", json=user_input)

    assert res.status_code == 201

    new_user = res.json()
    new_user["username"] = user_input["username"]
    new_user["password"] = user_input["password"]
    return new_user

@pytest.fixture(name="token")
def create_token(t_user):
    """Creates new JWT for a specific user"""
    return create_access_token({"username": t_user['username'], "id": t_user['id']})

@pytest.fixture(name="curr_user")
def authorized_client(token):
    """Returns token contents, mocking the cookie payload decode"""
    return verify_access_token(token)
