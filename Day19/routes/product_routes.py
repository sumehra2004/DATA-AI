
from flask import Blueprint, request
from models.product_model import create_product, get_all_products

product_bp = Blueprint("product", __name__)

@product_bp.route("/products", methods=["POST"])
def add_product():
    return create_product(request.json)

@product_bp.route("/products", methods=["GET"])
def get_products():
    return get_all_products()
