# pylint: disable=W0611
from jose import jwt
import pytest
from ..settings import env


def test_register_user(client):
    """Tests User Registration Endpoint"""
    res = client.post("/users/new", json={"username": "test", "password": "testing"})

    assert res.status_code == 201
    assert res.json()["message"] == "Created new user test"


def test_login(client, test_user):
    """Tests user login"""
    res = client.post("/login", data=test_user)

    # Check payload
    token = res.cookies.get("wsn-session")
    payload = jwt.decode(token, env.jwt_secret_key, algorithms=[env.jwt_algo])
    username: str = payload.get("username")

    assert res.status_code == 200
    assert username == test_user["username"]


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("wrong_user", "testing", 403),
        ("tester0", "wrong_pw", 403),
        ("wrong_user", "wrong_pw", 403),
        (None, "testing", 422),
        ("tester0", None, 422),
    ],
)
def test_login_fail(client, username, password, status_code):
    """Test case for failed login"""
    res = client.post("/login", data={"username": username, "password": password})

    assert res.status_code == status_code


def test_logout(client, curr_user_cookie):
    """Test case for logging out"""
    res = client.post("/logout", cookies=curr_user_cookie)

    assert res.status_code == 200
