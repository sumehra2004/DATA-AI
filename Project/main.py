from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uuid

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

users = {}
items = []
cart = []
current_order = None

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse("/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if users.get(username) == password:
        request.session["user"] = username
        return RedirectResponse("/home", status_code=302)
    return RedirectResponse("/login", status_code=302)

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    users[username] = password
    return RedirectResponse("/login", status_code=302)

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    total = sum(item["price"] for item in cart)
    return templates.TemplateResponse("home.html", {"request": request, "items": items, "cart": cart, "total": total})

@app.post("/add-item")
def add_item(title: str = Form(...), description: str = Form(...), price: float = Form(...), stock: int = Form(...), category: str = Form(...)):
    item = {
        "id": len(items) + 1,
        "title": title,
        "description": description,
        "price": price,
        "stock": stock,
        "category": category,
    }
    items.append(item)
    return RedirectResponse("/home", status_code=302)

@app.post("/add-cart")
def add_cart(item_id: int = Form(...)):
    for item in items:
        if item["id"] == item_id and item["stock"] > 0:
            cart.append(item)
            item["stock"] -= 1
    return RedirectResponse("/home", status_code=302)

@app.get("/checkout", response_class=HTMLResponse)
def checkout(request: Request):
    total = sum(item["price"] for item in cart)
    return templates.TemplateResponse("checkout.html", {"request": request, "cart": cart, "total": total})

@app.post("/checkout", response_class=HTMLResponse)
def create_order(request: Request, name: str = Form(...), address: str = Form(...), payment_method: str = Form(...)):
    global current_order
    subtotal = sum(item["price"] for item in cart)
    order_id = "ORD-" + uuid.uuid4().hex[:10].upper()

    order_items = []
    for item in cart:
        order_items.append({
            "item_id": item["id"],
            "title": item["title"],
            "price": item["price"],
            "quantity": 1,
            "line_total": item["price"],
        })

    current_order = {
        "order_id": order_id,
        "customer": {
            "name": name,
            "address": address
        },
        "payment_method": payment_method,
        "subtotal": subtotal,
        "status": "PENDING_PAYMENT",
        "items": order_items
    }

    return templates.TemplateResponse("order.html", {"request": request, "order": current_order})

@app.post("/payment", response_class=HTMLResponse)
def payment(request: Request):
    global current_order, cart
    if current_order:
        current_order["status"] = "CONFIRMED"
        current_order["paid_via"] = current_order["payment_method"]
    cart.clear()
    return templates.TemplateResponse("payment.html", {"request": request, "order": current_order})
