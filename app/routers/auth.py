from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, util, oauth2


router = APIRouter(tags=['Authentication'])
db_dependency = Annotated[Session, Depends(get_db)]
oauth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post('/login', response_model=schemas.token)
def login(db: db_dependency, user_cred: oauth_dependency):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid Credentials")

    if not util.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_auth_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type":"bearer"}