from fastapi import APIRouter
from schemas import Product
from database import products_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def add_product(product: Product):
    products_db.append(product)
    return {"message": "Product added"}

@router.get("/")
def list_products():
    return products_db
