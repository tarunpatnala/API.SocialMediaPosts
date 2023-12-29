from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

class base_post(BaseModel):
    title: str
    content: str

class create_post(base_post):
    published: bool = True
    rating: Optional[int] = 0

class update_post_model(BaseModel):
    published: bool
    rating: Optional[int]

class user_response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class response_model(base_post):
    id: int
    created_at: datetime
    owner_id: int
    owner: user_response
    
    class Config:
        from_attributes = True

class posts_votes(BaseModel):
    Post: response_model
    votes: int

class user(BaseModel):
    email: EmailStr
    password: str


class user_login(BaseModel):
    email: EmailStr
    password: str

class token(BaseModel):
    access_token: str
    token_type: str

class token_data(BaseModel):
    id: Optional[str]


class votes(BaseModel):
    post_id: int
    vote_dir: int