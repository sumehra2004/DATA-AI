from fastapi import FastAPI
from routers import users, products, blogs, comments

app = FastAPI(title="Simple E-commerce API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(blogs.router)
app.include_router(comments.router)

@app.get("/")
def home():
    return {"message": "E-commerce API running 🚀"}
