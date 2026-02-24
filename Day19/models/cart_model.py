
from utils.db import db
from flask import jsonify
from datetime import datetime

cart = db["cart"]

def add_to_cart(data):
    cart.insert_one({
        "user_id": data["user_id"],
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "added_at": datetime.utcnow()
    })
    return jsonify({"message": "Added to cart"})
