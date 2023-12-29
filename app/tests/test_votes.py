import pytest
from .. import models

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[1].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorize_client, test_posts):
    res = authorize_client.post("/vote/", json={"post_id":test_posts[1].id, "vote_dir":1})
    assert res.status_code == 200

def test_vote_on_post_non_exist(authorize_client, test_posts):
    res = authorize_client.post("/vote/", json={"post_id":"99", "vote_dir":1})
    assert res.status_code == 404

def test_delete_vote_on_post(authorize_client, test_posts, test_vote):
    res = authorize_client.post("/vote/", json={"post_id":test_posts[1].id, "vote_dir":0})
    assert res.status_code == 200

def test_delete_vote_non_exist_post(authorize_client, test_posts):
    res = authorize_client.post("/vote/", json={"post_id":test_posts[2].id, "vote_dir":0})
    assert res.status_code == 404

def test_vote_twice_on_post(authorize_client, test_posts, test_vote):
    res = authorize_client.post("/vote/", json={"post_id":test_posts[1].id, "vote_dir":1})
    assert res.status_code == 302

def test_vote_others_post(authorize_client, test_posts):
    res = authorize_client.post("/vote/", json={"post_id":test_posts[3].id, "vote_dir":1})
    assert res.status_code == 200

def test_unauthorised_vote_on_post(client, test_posts):
    res = client.post("/vote/", json={"post_id":test_posts[1].id, "vote_dir":1})
    assert res.status_code == 401