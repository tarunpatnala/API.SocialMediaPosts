from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, util, oauth2


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.token)
def login(user_cred: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid Credentials")

    if not util.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_auth_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type":"bearer"}