
from flask import Blueprint, request
from models.cart_model import add_to_cart

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart/add", methods=["POST"])
def add_cart():
    return add_to_cart(request.json)
