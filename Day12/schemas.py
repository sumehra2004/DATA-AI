from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Product(BaseModel):
    name: str
    price: float
    category: str

class Blog(BaseModel):
    title: str
    content: str

class Comment(BaseModel):
    text: str
