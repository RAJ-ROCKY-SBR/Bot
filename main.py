
from flask import Flask, request, render_template, jsonify
import openai
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, user TEXT, bot TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_msg = request.form["message"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_msg,
        max_tokens=150
    )
    bot_msg = response.choices[0].text.strip()

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (user, bot) VALUES (?, ?)", (user_msg, bot_msg))
    conn.commit()
    conn.close()

    return jsonify({"response": bot_msg})

if __name__ == "__main__":
    app.run(debug=True)
