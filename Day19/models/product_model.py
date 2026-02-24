
from utils.db import db
from flask import jsonify
from datetime import datetime
from bson import ObjectId

products = db["products"]

def create_product(data):
    if data["price"] <= 0:
        return jsonify({"error": "Price must be greater than 0"}), 400

    product = {
        "name": data["name"],
        "description": data["description"],
        "price": data["price"],
        "category": data["category"],
        "stock": data["stock"],
        "image_url": data["image_url"],
        "created_at": datetime.utcnow()
    }

    products.insert_one(product)
    return jsonify({"message": "Product added"})

def get_all_products():
    product_list = list(products.find())
    for p in product_list:
        p["_id"] = str(p["_id"])
    return jsonify(product_list)
