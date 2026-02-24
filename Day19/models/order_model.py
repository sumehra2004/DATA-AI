
from utils.db import db
from flask import jsonify
from datetime import datetime

orders = db["orders"]
cart = db["cart"]

def place_order(user_id):
    items = list(cart.find({"user_id": user_id}))
    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    total_price = 0
    order_products = []

    for item in items:
        order_products.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": 0
        })

    order = {
        "user_id": user_id,
        "products": order_products,
        "total_price": total_price,
        "status": "Placed",
        "created_at": datetime.utcnow()
    }

    orders.insert_one(order)
    cart.delete_many({"user_id": user_id})

    return jsonify({"message": "Order placed successfully"})
