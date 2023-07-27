from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author, text):
        self.author = author
        self.text = text

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text
        }


# dict --> JSON - сериализация
# JSON --> dict - десериализация
# Object --> dict --> JSON
@app.route("/quotes")
def get_quotes():
    quotes: list[QuoteModel] = QuoteModel.query.all()
    quotes_dict: list[dict] = []
    for quote in quotes:
        quotes_dict.append(quote.to_dict())
    return quotes_dict
