def test_add_like(client, post_content, curr_user_cookie, other_user_cookie):
    """Test case for liking a reply"""
    # Create post
    post = client.post("/posts/new", json=post_content, cookies=curr_user_cookie).json()
    # Create reply
    reply = client.post(
        f"/replies/{post['id']}", json=post_content, cookies=other_user_cookie
    ).json()
    # Like post
    like_body = {"reply_id": int(reply["id"]), "cmd": 1}
    res = client.post("/like/", json=like_body, cookies=curr_user_cookie)

    assert res.status_code == 200
    assert res.json()['message'] == "successfully liked the reply."

def test_fail_add_like(client, post_content, curr_user_cookie, other_user_cookie):
    """Test case for liking a reply twice. Should return 409 CONFLICT error"""
    # Create post
    post = client.post("/posts/new", json=post_content, cookies=curr_user_cookie).json()
    # Create reply
    reply = client.post(
        f"/replies/{post['id']}", json=post_content, cookies=other_user_cookie
    ).json()
    # Like post
    like_body = {"reply_id": int(reply["id"]), "cmd": 1}
    client.post("/like/", json=like_body, cookies=curr_user_cookie)
    res = client.post("/like/", json=like_body, cookies=curr_user_cookie)

    assert res.status_code == 409

def test_remove_like(client, post_content, curr_user_cookie, other_user_cookie):
    """Test case for unliking a reply."""
    # Create post
    post = client.post("/posts/new", json=post_content, cookies=curr_user_cookie).json()
    # Create reply
    reply = client.post(
        f"/replies/{post['id']}", json=post_content, cookies=other_user_cookie
    ).json()
    # Like post
    like_body = {"reply_id": int(reply["id"]), "cmd": 1}
    unlike_body = {"reply_id": int(reply["id"]), "cmd": 0}
    client.post("/like/", json=like_body, cookies=curr_user_cookie)
    res = client.post("/like/", json=unlike_body, cookies=curr_user_cookie)

    assert res.status_code == 204

def test_fail_remove_like(client, post_content, curr_user_cookie, other_user_cookie):
    """Test case for unliking a reply when none exists."""
    # Create post
    post = client.post("/posts/new", json=post_content, cookies=curr_user_cookie).json()
    # Create reply
    reply = client.post(
        f"/replies/{post['id']}", json=post_content, cookies=other_user_cookie
    ).json()
    # Like post
    unlike_body = {"reply_id": int(reply["id"]), "cmd": 0}
    res = client.post("/like/", json=unlike_body, cookies=curr_user_cookie)

    assert res.status_code == 404
