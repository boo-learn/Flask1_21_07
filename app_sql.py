import sqlite3
from pathlib import Path
from flask import g
from flask import Flask, json, request

app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / 'test.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def tuple_to_dict(quote: tuple) -> dict:
    keys = ["id", "author", "text"]

    return dict(zip(keys, quote))


def get_object_from_db(sql: str) -> dict:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute(sql)
    object = cursor.fetchone()
    object = tuple_to_dict(object)
    cursor.close()
    connection.close()
    return object


def get_objects_from_db(sql: str) -> list[dict]:
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute(sql)
    objects = cursor.fetchall()
    objects = list(map(tuple_to_dict, objects))
    cursor.close()
    connection.close()
    return objects


@app.route("/quotes")
def get_quotes():
    select_quotes = "SELECT * from quotes"
    quotes = get_objects_from_db(select_quotes)
    return quotes


@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    sql = f"SELECT * FROM quotes WHERE id={quote_id}"
    quote = get_object_from_db(sql)
    return quote


@app.route("/quotes/count")
def quotes_count():
    return {
        "count": len(quotes)
    }


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    connection = get_db()
    cursor = connection.cursor()
    sql = f"INSERT INTO quotes (author, text) VALUES ('{new_quote['author']}', '{new_quote['text']}');"
    cursor.execute(sql)
    connection.commit()
    new_quote["id"] = cursor.lastrowid
    return new_quote, 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    new_data = request.json
    for quote in quotes:
        if quote["id"] == quote_id:
            if new_data.get("author"):
                quote["author"] = new_data["author"]
            if new_data.get("text"):
                quote["text"] = new_data["text"]
            return quote, 200

    return f"Quote with id={quote_id} not found", 404
