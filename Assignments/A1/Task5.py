from flask import Flask, render_template_string

app = Flask(__name__)

# -----------------------
# Static Blog Data
# -----------------------
blogs = [
    {
        "id": 1,
        "title": "Introduction to Python",
        "author": "Admin",
        "content": "Python is a powerful and easy-to-learn programming language.",
    },
    {
        "id": 2,
        "title": "Flask for Beginners",
        "author": "Admin",
        "content": "Flask is a lightweight Python web framework.",
    },
    {
        "id": 3,
        "title": "Understanding Templates",
        "author": "Admin",
        "content": "Templates allow dynamic HTML rendering using data.",
    },
]

# -----------------------
# Blog List Page
# -----------------------
@app.route("/")
def blog_list():
    template = """
    <h1>Blog List</h1>
    <ul>
        {% for blog in blogs %}
            <li>
                <h3>
                    <a href="/blog/{{ blog.id }}">{{ blog.title }}</a>
                </h3>
                <small>By {{ blog.author }}</small>
            </li>
        {% endfor %}
    </ul>
    """
    return render_template_string(template, blogs=blogs)


# -----------------------
# Blog Detail Page
# -----------------------
@app.route("/blog/<int:blog_id>")
def blog_detail(blog_id):
    blog = next((b for b in blogs if b["id"] == blog_id), None)

    template = """
    {% if blog %}
        <h1>{{ blog.title }}</h1>
        <p><strong>Author:</strong> {{ blog.author }}</p>
        <hr>
        <p>{{ blog.content }}</p>
        <br>
        <a href="/">← Back to Blog List</a>
    {% else %}
        <h2>Blog not found</h2>
        <a href="/">Back</a>
    {% endif %}
    """
    return render_template_string(template, blog=blog)


# -----------------------
# Run App
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)