from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from models import Electronics, Grocery
from inventory import Inventory

app = FastAPI()
templates = Jinja2Templates(directory="templates")

inventory = Inventory()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": inventory.products}
    )


@app.post("/add")
def add_product(
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    type: str = Form(...)
):
    if type == "Electronics":
        product = Electronics(name, price, stock)
    else:
        product = Grocery(name, price, stock)

    inventory.add_product(product)
    return {"message": "Product added"}


@app.post("/remove")
def remove_product(name: str = Form(...)):
    inventory.remove_product(name)
    return {"message": "Removed"}


@app.post("/update")
def update_stock(name: str = Form(...), stock: int = Form(...)):
    inventory.update_stock(name, stock)
    return {"message": "Updated"}


@app.get("/search")
def search(name: str):
    p = inventory.search_product(name)
    if p:
        return p.to_dict()
    return {"message": "Not found"}
