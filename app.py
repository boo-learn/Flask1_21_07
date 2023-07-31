from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path

BASE_DIR = Path(__file__).parent
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author, text):
        self.author_id = author.id
        self.text = text

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author.to_dict()
        }


# AUTHORS
# /authors  <--- all authors
@app.route("/authors")
def get_authors():
    authors = AuthorModel.query.all()

    authors_dict = [author.to_dict() for author in authors]
    return authors_dict


@app.route("/authors/<int:author_id>")
def get_author_by_id(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        return f"Author with id={author_id} not found", 404
    return author.to_dict(), 200


@app.route("/authors", methods=["POST"])
def create_author():
    new_author = request.json
    author = AuthorModel(**new_author)
    db.session.add(author)
    db.session.commit()
    return author.to_dict(), 201


# QUOTES

# Сериализация:
# Object --> dict --> JSON
@app.route("/quotes")
def get_quotes():
    quotes = QuoteModel.query.all()
    quotes_dict = [quote.to_dict() for quote in quotes]
    return quotes_dict


@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        return f"Quote with id={quote_id} not found", 404
    return quote.to_dict(), 200


@app.route("/authors/<int:author_id>/quotes", methods=["POST"])
def create_quote(author_id):
    author = AuthorModel.query.get(author_id)
    new_quote = request.json
    quote = QuoteModel(author, **new_quote)
    db.session.add(quote)
    db.session.commit()
    return quote.to_dict(), 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    new_data = request.json
    # TODO: реализовать редактирование цитаты
    return ..., 200


@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    # TODO: реализовать удаление цитаты
    return "", 204
