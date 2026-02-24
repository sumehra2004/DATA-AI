from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_super_secret_key'

# Temporary in-memory user storage
users = {}

# -----------------------------
# Token Required Decorator
# -----------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Token in header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# -----------------------------
# Register Route
# -----------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if username in users:
        return jsonify({'message': 'User already exists!'})

    hashed_password = generate_password_hash(password)

    users[username] = hashed_password

    return jsonify({'message': 'User registered successfully!'})

# -----------------------------
# Login Route
# -----------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if username not in users:
        return jsonify({'message': 'User not found!'})

    if check_password_hash(users[username], password):

        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid password!'})

# -----------------------------
# Protected Route (GET)
# -----------------------------
@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        'message': 'Profile accessed successfully!',
        'username': current_user
    })

# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)