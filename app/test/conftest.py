from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
# Fixtures are duplicated for each user as many interactions require more than one user

# User 0
@pytest.fixture(name="test_user", scope="module")
def create_test_user(client):
    """Create test user for login endpoint"""
    user_input = {"username": "tester0", "password": "testing"}
    res = client.post("users/new", json=user_input)

    assert res.status_code == 201

    new_user = res.json()
    new_user["username"] = user_input["username"]
    new_user["password"] = user_input["password"]
    return new_user


# User 1
@pytest.fixture(name="other_user", scope="module")
def create_test_user1(client):
    """Create test user for login endpoint"""
    user_input = {"username": "tester1", "password": "testing"}
    res = client.post("users/new", json=user_input)

    assert res.status_code == 201

    new_user = res.json()
    new_user["username"] = user_input["username"]
    new_user["password"] = user_input["password"]
    return new_user


# User 0
@pytest.fixture(name="curr_user_cookie")
def login_with_test_user(client, test_user):
    """Login with test user and return cookie"""
    res = client.post("/login", data=test_user)

    assert res.status_code == 200

    cookie = {"wsn-session": res.json()["token"]}

    return cookie


# User 1
@pytest.fixture(name="other_user_cookie")
def login_with_test_user1(client, other_user):
    """Login with test user and return cookie"""
    res = client.post("/login", data=other_user)

    assert res.status_code == 200

    cookie = {"wsn-session": res.json()["token"]}

    return cookie


# Post Fixtures


@pytest.fixture(name="post_content", scope="module")
def create_post_input():
    """Returns generic post content for tests"""
    return {"title": "My Post Title", "content": "My Post Content."}

# User 0
@pytest.fixture(name="new_post")
def create_new_post(client, curr_user_cookie, post_content):
    """Create new post for tests"""
    res = client.post("/posts/new", json=post_content, cookies=curr_user_cookie)

    assert res.status_code == 201
    assert res.json()["title"] == post_content["title"]

    return res.json()

# User 1
@pytest.fixture(name="other_new_post")
def create_new_post1(client, other_user_cookie, post_content):
    """Create new post for tests"""
    res = client.post("/posts/new", json=post_content, cookies=other_user_cookie)

    assert res.status_code == 201
    assert res.json()["title"] == post_content["title"]

    return res.json()
