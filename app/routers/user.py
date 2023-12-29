from .. import models, schemas, util
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.user_response)
async def create_user(user: schemas.user, db: Session=Depends(get_db)):
    #hash password
    user.password = util.hash(user.password)

    request_model = models.User(**user.model_dump(),)
    db.add(request_model)
    db.commit()
    db.refresh(request_model)
    return request_model

@router.get("/{id}", response_model=schemas.user_response)
async def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user