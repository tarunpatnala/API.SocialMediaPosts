from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2, models, schemas

router = APIRouter(tags=["Vote"], prefix="/vote")

@router.post("/")
async def vote(payload: schemas.votes, current_user: str = Depends(oauth2.get_current_user), db: Session=Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id==payload.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{payload.post_id} does not exist")

    vote_exist = db.query(models.Vote).filter(models.Vote.post_id==payload.post_id, models.Vote.user_id==current_user.id)
    
    if payload.vote_dir == 1:
        if vote_exist.first() != None:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Already Voted")
        vote_request = models.Vote(user_id=current_user.id, post_id=payload.post_id)
        db.add(vote_request)
        db.commit()
        return {"message":"Successfully added a vote"}
    if payload.vote_dir == 0:
        if vote_exist.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote doesn't exist")
        vote_exist.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted a vote"}
