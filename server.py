from flask import Flask, request, abort
from saver import *
import json

PATH = "SAVE.json"

app = Flask(__name__)

# try:
#     with open(PATH, "r") as fh:
#         database = json.load(fh)
# except:
database = []


@app.route("/")
def hello():
    return "Hello this is sever of PA"

# Получаем сюда информацию с клиента и обрабатываем ее.


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    # validation data first stage
    if not isinstance(data, dict):
        return abort(400)
    if 'text' not in data:
        return abort(400)

    text = data['text']

    # validation data - second stage
    if not isinstance(text, str):
        return abort(400)
    if not (0 < len(text) < 1000):
        return abort(400)

    message = {
        'text': text
    }
    database.append(message)

    with open(PATH, "w") as fh:
        json.dump(database, fh)

    return {"ok": True}

# отправляем на запрос информацию клиенту.


@app.route("/messages", methods=['GET'])
def get_message():

    messages = []
    for message in database:
        messages.append(message)

    return {"messages": messages[:50]}


app.run()
