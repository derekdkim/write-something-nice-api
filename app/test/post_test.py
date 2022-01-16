# pylint: disable=W0611
import pytest


def test_create_post(client, curr_user_cookie, post_content):
    """Test case for creating post"""
    res = client.post("/posts/new", json=post_content, cookies=curr_user_cookie)

    assert res.status_code == 201
    assert res.json()["title"] == post_content["title"]


def test_fail_create_post(client, curr_user_cookie):
    """Test case for failing to create post"""
    res = client.post(
        "/posts/new",
        json={"title": None, "content": "My Post Content."},
        cookies=curr_user_cookie,
    )

    assert res.status_code == 422


def test_update_post(client, curr_user_cookie, new_post):
    """Test case for updating post"""
    updated_content = {"title": "Updated Post", "content": "Hello World"}
    res = client.put(
        f"/posts/{new_post['id']}", json=updated_content, cookies=curr_user_cookie
    )

    res_post = res.json()
    assert res.status_code == 200
    assert res_post["title"] == updated_content["title"]
    assert res_post["content"] == updated_content["content"]


def test_delete_post(client, curr_user_cookie, new_post):
    """Test case for deleting post"""
    res = client.delete(f"/posts/{new_post['id']}", cookies=curr_user_cookie)

    assert res.status_code == 204


def test_get_own_posts(
    client, post_content,
):
    """Test case for retrieving only the user's posts"""
    # Register new user
    client.post("/users/new", json={"username": "Adam", "password": "Sandler"})
    # Login
    login = client.post("/login", data={"username": "Adam", "password": "Sandler"})
    cookie = {"wsn-session": login.json()["token"]}
    # Create 3 posts
    client.post("/posts/new", json=post_content, cookies=cookie)
    client.post("/posts/new", json=post_content, cookies=cookie)
    client.post("/posts/new", json=post_content, cookies=cookie)

    res = client.get("/posts/current-user", cookies=cookie)

    assert res.status_code == 200

    posts = res.json()
    assert len(posts) == 3

def test_get_active_posts(client, curr_user_cookie, test_user):
    """Test case for user getting other users' posts"""
    res = client.get("/posts/active", cookies=curr_user_cookie)

    assert res.status_code == 200

    posts = res.json()
    for post in posts:
        assert int(post['author_id']) != int(test_user['id'])

def test_get_random_post(client, curr_user_cookie, post_content, test_user):
    """Test case for getting random post"""
    # Register new user
    client.post("/users/new", json={"username": "John", "password": "Doe"})
    # Login
    login = client.post("/login", data={"username": "John", "password": "Doe"})
    cookie = {"wsn-session": login.json()["token"]}
    # Create 3 posts
    client.post("/posts/new", json=post_content, cookies=cookie)
    client.post("/posts/new", json=post_content, cookies=cookie)
    client.post("/posts/new", json=post_content, cookies=cookie)

    # Don't have a really good way of checking for randomness without having a very big test
    # Keeping it basic for now
    res = client.get("/posts/random", cookies=curr_user_cookie)

    assert res.status_code == 200
    assert int(res.json()['author_id']) != int(test_user['id'])
