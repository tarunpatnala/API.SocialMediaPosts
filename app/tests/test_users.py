from .. import schemas
from jose import jwt
from ..config import settings
import pytest

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Welcome to Amature Posts!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email":"tarunpatnala@gmail.com", "password":"Tarun1995"})
    new_user = schemas.user_response(**res.json())
    assert new_user.email == "tarunpatnala@gmail.com"
    assert res.status_code == 201

def test_login(test_user, client):
    res = client.post("/login", data={"username":test_user['email'], "password":test_user['password']})
    assert res.status_code == 200
    login_res = schemas.token(**res.json())
    payload = jwt.decode(token=login_res.access_token, key=settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
        ("wronge@gmail.com", "Tarun1995", 403),
        ("tarunpatnala@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "Tarun1995", 422),
        ("testuser@gmail.com", None, 422)
])
def test_failed_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username":email, "password":password})
    assert res.status_code == status_code