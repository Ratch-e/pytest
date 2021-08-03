from flask import Flask, request, render_template
from datetime import datetime
import getpass
import json
import time
import flask

app = Flask(__name__)

db_file = './db/db.json'
data = json.load(open(db_file, "rb"))
db = data["messages"]


def save_messages():
    json.dump({
        "messages": db
    }, open(db_file, "w"))


@app.route("/")
def index_page():
    return "Hello"


@app.route("/admin_delete_everything")
def clear_messages():
    password = request.args.get("password")

    if password == "123":
        json.dump({
            "messages": []
        }, open(db_file, "w"))
        return "messages cleared"

    return "password required"


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/sendMessage")
def chat():
    name = request.args["name"]
    text = request.args["text"]

    name_len = len(name)
    text_len = len(text)

    if name_len > 100 or name_len < 3:
        return "Error"

    if text_len == 0 or text_len > 3000:
        return "Error2"

    db.append({
        "name": name,
        "text": text,
        "time": time.time()
    })

    save_messages()
    return "Message saved"


@app.route("/messages")
def get_messages():
    after_timestamp = float(request.args['stamp'])
    result = []
    for message in db:
        if message["time"] > after_timestamp:
            result.append(message)

    return {"messages": result}


@app.route("/status")
def get_status():
    name = Flask.__name__
    version = flask.__version__
    username = getpass.getuser()
    cur_time = datetime.now().time().replace(microsecond=0)

    return f"({name}:{version}) {username}, {cur_time} ~ Messages in local DB: {len(db)}"


app.run()
