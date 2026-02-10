from app import app, db
with app.app_context():
    db.create_all()



@app.route("/add-user")
def add_user():
    user = User(username="alice", email="alice@test.com")
    db.session.add(user)
    db.session.commit()
    return "User added"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship("Post", backref="author")
