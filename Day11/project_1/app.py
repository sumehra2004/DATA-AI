from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models import User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add-user", methods=["POST"])
def add_user():
    username = request.form.get("username")
    email = request.form.get("email")

    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("users"))

@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
