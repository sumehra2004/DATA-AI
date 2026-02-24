from fastapi import APIRouter
from schemas import Comment
from database import comments_db

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/")
def add_comment(comment: Comment):
    comments_db.append(comment)
    return {"message": "Comment added"}
