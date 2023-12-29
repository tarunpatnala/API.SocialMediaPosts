from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)

@router.get("/", response_model=List[schemas.posts_votes])
async def get_posts(current_user: str = Depends(oauth2.get_current_user), db: Session=Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    #db_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).offset(skip).all()
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.response_model)
async def create_posts(payLoad: schemas.create_post, current_user: str = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    new_post = models.Post(owner_id=current_user.id,**payLoad.model_dump(),)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model=schemas.posts_votes)
async def get_latest_post(current_user: str = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    latest_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.owner_id==current_user.id).group_by(models.Post.id).order_by(models.Post.id.desc()).limit(1).first()
    return latest_post

@router.get("/{id}", response_model=schemas.posts_votes)
async def get_post(id: int, response: Response, current_user: str = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: str = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.response_model)
async def update_post(id: int, post: schemas.update_post_model, current_user: str = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist.")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()