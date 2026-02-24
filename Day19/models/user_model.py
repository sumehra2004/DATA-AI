
from utils.db import db
from flask import jsonify
import bcrypt
from datetime import datetime

users = db["users"]

def create_user(data):
    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,
        "phone": data["phone"],
        "address": data["address"],
        "created_at": datetime.utcnow()
    }

    users.insert_one(user)
    return jsonify({"message": "User registered successfully"})
