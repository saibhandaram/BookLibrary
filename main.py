from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.FLOAT, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = []
    with app.app_context():
        result = db.session.execute(db.select(Book))
        # print(result)
        all_books = result.scalars().all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # books_dict = {
        #     "title": f"{request.form['book_name']}",
        #     "author": f"{request.form['book_author']}",
        #     "rating": f"{request.form['book_rating']}"
        # }
        #
        # all_books.append(books_dict)
        # print(all_books)
        # CREATE RECORD
        with app.app_context():
            new_book = Book(title=request.form['book_name'], author=request.form['book_author'],
                            rating=request.form['book_rating'])
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/delete/<int:book_id>", )
def delete_book(book_id):
    # book_id = 1
    print(f"Book ID for Delete is : {book_id}")
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        # or book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit/<int:book_id>", methods=['GET', 'POST'])
def edit_rating(book_id):
    if request.method == 'GET':
        with app.app_context():
            book_to_edit = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
            print(book_to_edit)
        return render_template('edit.html', book_info=book_to_edit)
    else:
        with app.app_context():
            book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
            # or book_to_update = db.get_or_404(Book, book_id)
            book_to_update.rating = request.form['new_rating']
            db.session.commit()

        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
