from fastapi import APIRouter
from schemas import User
from database import users_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register(user: User):
    users_db.append(user)
    return {"message": "User registered"}

@router.post("/login")
def login(user: User):
    for u in users_db:
        if u.username == user.username and u.password == user.password:
            return {"message": "Login successful"}
    return {"error": "Invalid credentials"}
