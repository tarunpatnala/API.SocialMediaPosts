from .. import schemas
import pytest

def test_get_all_posts(authorize_client, test_posts):
    res = authorize_client.get("/posts/")
    posts = res.json()
    for p,q in zip(posts,test_posts):
       single_post = schemas.posts_votes(**p)
       assert single_post.Post.id == q.id
       assert single_post.Post.title == q.title
       assert single_post.Post.content == q.content
    assert len(posts) == len(test_posts)
    assert res.status_code == 200

def test_unauthorised_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorised_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorize_client):
    res = authorize_client.get("/posts/100")
    assert res.status_code == 404

def test_get_one_post(authorize_client, test_posts):
    res = authorize_client.get(f"/posts/{test_posts[1].id}")
    assert res.status_code == 200
    res_post = schemas.posts_votes(**res.json())
    assert res_post.Post.id == test_posts[1].id
    assert res_post.Post.title == test_posts[1].title
    assert res_post.Post.content == test_posts[1].content

@pytest.mark.parametrize("title, content, published, rating", [("test post", "This is a post created by test", True, 4)])
def test_create_post(authorize_client, title, content, published, rating, test_user):
    res = authorize_client.post("/posts/", json={"title":title, "content":content, "published":published, "rating":rating, "owner_id":test_user['id']})
    assert res.status_code == 201
    res_post = schemas.response_model(**res.json())
    assert res_post.title == title
    assert res_post.content == content
    assert res_post.owner_id == test_user['id']

@pytest.mark.parametrize("title, content", [("test post", "This is a post created by test")])
def test_create_post_default_published_rating(authorize_client, title, content, test_user):
    res = authorize_client.post("/posts/", json={"title":title, "content":content, "owner_id":test_user['id']})
    assert res.status_code == 201
    res_post = schemas.response_model(**res.json())
    assert res_post.title == title
    assert res_post.content == content
    assert res_post.published == True
    assert res_post.rating == 0
    assert res_post.owner_id == test_user['id']


def test_unauthorised_user_create_post(client, test_user):
    res = client.post("/posts/", json={"title":"Testing", "content":"Testing 12345678", "owner_id":test_user['id']})
    assert res.status_code == 401

def test_unauthorised_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorize_client, test_posts):
    res = authorize_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorize_client, test_posts):
    res = authorize_client.delete("/posts/100")
    assert res.status_code == 404

def test_delete_other_user_post(authorize_client, test_posts):
    res = authorize_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorize_client, test_user, test_posts):
    data = {
        "id": test_posts[0].id,
        "published": False,
        "rating": 5
    }
    res = authorize_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_res = schemas.response_model(**res.json())
    assert res.status_code == 200
    assert update_res.id == test_posts[0].id
    assert update_res.published == data['published']
    assert update_res.rating == data['rating']

def test_update_other_user_post(authorize_client, test_posts):
    data = {
        "id": test_posts[3].id,
        "published": False,
        "rating": 5
    }
    res = authorize_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorised_update_post(client, test_posts):
    data = {
        "id": test_posts[3].id,
        "published": False,
        "rating": 5
    }
    res = client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 401