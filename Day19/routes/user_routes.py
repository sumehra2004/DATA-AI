
from flask import Blueprint, request
from models.user_model import create_user

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    return create_user(request.json)
