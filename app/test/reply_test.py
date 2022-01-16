def test_create_reply(client, other_new_post, curr_user_cookie, test_user):
    """Test case for creating a new reply"""
    reply_content = {"title": "just testing", "content": "yes"}
    # Create reply
    res = client.post(
        f"/replies/{other_new_post['id']}", json=reply_content, cookies=curr_user_cookie
    )
    reply = res.json()

    assert res.status_code == 201
    assert reply["title"] == reply_content["title"]
    assert reply["author_id"] == test_user["id"]
    assert reply["post_id"] == other_new_post["id"]


# Get replies
def test_get_replies(
    client, post_content, other_new_post, curr_user_cookie, test_user, other_user_cookie
):
    """Test case for getting replies"""
    # Create replies
    client.post(
        f"/replies/{other_new_post['id']}", json=post_content, cookies=curr_user_cookie
    )
    client.post(
        f"/replies/{other_new_post['id']}", json=post_content, cookies=curr_user_cookie
    )
    # Get replies
    res = client.get(f"/replies/{other_new_post['id']}", cookies=other_user_cookie)
    replies = res.json()

    assert res.status_code == 200
    assert len(replies) == 2
    for reply in replies:
        assert int(reply["author_id"]) == int(test_user["id"])


# Update reply
def test_update_reply(client, post_content, new_post, other_user_cookie):
    """Test case for updating reply"""
    updated_content = {"title": "Hello World", "content": "this is updated."}
    # Create reply
    reply = client.post(
        f"/replies/{new_post['id']}", json=post_content, cookies=other_user_cookie
    )
    res = client.put(
        f"/replies/{reply.json()['id']}",
        json=updated_content,
        cookies=other_user_cookie,
    )

    assert res.status_code == 200
    assert res.json()["content"] == updated_content["content"]

# Delete reply
def test_delete_reply(client, post_content, new_post, other_user_cookie):
    """Test case for deleting reply"""
    # Create reply
    reply = client.post(
        f"/replies/{new_post['id']}", json=post_content, cookies=other_user_cookie
    )
    res = client.delete(
        f"/replies/{reply.json()['id']}",
        cookies=other_user_cookie,
    )

    assert res.status_code == 204
