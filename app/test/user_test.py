def test_get_user_profile(client, post_content, curr_user_cookie, other_user_cookie, other_user):
    """Test case for fetching user's info, including their total reputation/likes"""
    # Create post
    post = client.post("/posts/new", json=post_content, cookies=curr_user_cookie).json()
    # Create reply
    reply = client.post(
        f"/replies/{post['id']}", json=post_content, cookies=other_user_cookie
    ).json()
    # Like post
    like_body = {"reply_id": int(reply["id"]), "cmd": 1}
    client.post("/like/", json=like_body, cookies=curr_user_cookie)

    res = client.get("/users/", cookies=other_user_cookie)
    profile = res.json()

    assert res.status_code == 200
    assert profile['likes'] == 1
    assert profile['User']['username'] == other_user['username']