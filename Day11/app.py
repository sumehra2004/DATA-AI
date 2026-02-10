from flask import Flask, request,redirect, url_for,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/about")
def about():
    return "About page"


@app.route("/name")
def homes():
    return render_template("index.html", name="Sam")


@app.route("/login", methods=["GET", "POST"])
def login():
    return "Login"

@app.route("/user/<name>")
def user(name):
    return f"Hello {name}"



@app.route("/form")
def fo():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    return f"Welcome {username}"


if __name__ == "__main__":
    app.run(debug=True)
