from fastapi import APIRouter
from schemas import Blog
from database import blogs_db

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.post("/")
def create_blog(blog: Blog):
    blogs_db.append(blog)
    return {"message": "Blog created"}

@router.get("/")
def get_blogs():
    return blogs_db
