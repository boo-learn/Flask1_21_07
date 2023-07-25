from flask import Flask, json, request

app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False

about_me = {
    "name": "Евгений",
    "surname": "Юрченко",
    "email": "eyurchenko@specialist.ru"
}

quotes = [
    {
        "id": 3,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
    },
    {
        "id": 5,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 6,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 8,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    },

]


@app.route("/")
def hello_world():
    return "<p>Hello, World!!!</p>"


# http://127.0.0.1:5000/about
@app.route("/about")
def about_author():
    return about_me


# GET: http://127.0.0.1:5000/quotes
@app.route("/quotes")
def get_quotes():
    return quotes


# http://127.0.0.1:5000/quotes/2
# http://127.0.0.1:5000/quotes/5
# http://127.0.0.1:5000/quotes/10
# http://127.0.0.1:5000/quotes/50
@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote

    return f"Quote with id={quote_id} not found", 404


@app.route("/quotes/count")
def quotes_count():
    return {
        "count": len(quotes)
    }


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    new_id = quotes[-1]["id"] + 1
    new_quote["id"] = new_id
    quotes.append(new_quote)
    return new_quote, 201
