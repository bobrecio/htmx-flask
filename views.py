from app import app, db
from flask import render_template, request, jsonify
from app.models import Author, Book


@app.route("/", methods=["GET"])
def home():
    books = (
        db.session.query(Book, Author).filter(Book.author_id == Author.author_id).all()
    )
    return render_template("index.html", books=books)


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return ""


@app.route("/update/<int:id>", methods=["PUT"])
def update_book(id):
    db.session.query(Book).filter(Book.book_id == id).update(
        {"title": request.form["title"]}
    )
    db.session.commit()

    title = request.form["title"]
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    response = f"""
    <tr>
        <td>{title}</td>
        <td>{author.name}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response
