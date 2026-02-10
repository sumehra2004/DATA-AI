import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db, login_manager
from models import User, Product

# ------------------
# APP CONFIG
# ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")

db.init_app(app)
login_manager.init_app(app)

# ------------------
# LOGIN MANAGER
# ------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------
# ROUTES
# ------------------
@app.route("/", methods=["GET"])
@login_required
def products():
    search = request.args.get("search")
    max_price = request.args.get("price")

    query = Product.query
    if search:
        query = query.filter(Product.name.contains(search))
    if max_price:
        query = query.filter(Product.price <= max_price)

    return render_template("products.html", products=query.all())

# ------------------
# AUTH
# ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            login_user(user)
            return redirect(url_for("products"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# ------------------
# ADD PRODUCT (ADMIN)
# ------------------
@app.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    if not current_user.is_admin:
        return "Unauthorized", 403

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        image = request.files["image"]

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        product = Product(
            name=name,
            price=price,
            image=filename
        )
        db.session.add(product)
        db.session.commit()

        return redirect(url_for("products"))

    return render_template("add_products.html")

# ------------------
# MAIN
# ------------------
if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.app_context():
        db.create_all()

        # create admin if not exists
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                password="admin",
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
