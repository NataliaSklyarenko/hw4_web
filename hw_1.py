from flask import Flask, render_template, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Шлях до директорії для збереження файлів
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')
# Шлях до файлу з даними
DATA_FILE = os.path.join(STORAGE_DIR, 'data.json')

# Перевірка наявності директорії для збереження файлів, якщо її немає - створюємо
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

# Перевірка наявності файлу з даними, якщо його немає - створюємо
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    # Отримуємо дані з форми
    username = request.form['username']
    message = request.form['message']

    # Отримуємо поточну дату та час
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")

    # Створюємо словник для збереження даних
    data = {
        "username": username,
        "message": message
    }

    # Зчитуємо дані з файлу
    with open(DATA_FILE, 'r') as f:
        messages = json.load(f)

    # Додаємо нове повідомлення
    messages[timestamp] = data

    # Зберігаємо оновлені дані у файл
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

    return 'Message received!'

if __name__ == '__main__':
    app.run(debug=True, port=3000)
