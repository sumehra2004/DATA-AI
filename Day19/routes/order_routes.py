
from flask import Blueprint
from models.order_model import place_order

order_bp = Blueprint("order", __name__)

@order_bp.route("/order/<user_id>", methods=["POST"])
def order(user_id):
    return place_order(user_id)
