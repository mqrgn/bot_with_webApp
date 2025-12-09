import os
import sqlite3

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


def get_user_data(user_id):
    try:
        DB_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../WebTgDB.db"))

        connect = sqlite3.connect(DB_PATH)
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()

        cursor.execute("SELECT color, car FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            return dict(user)
        return None

    except Exception as e:
        print(f"Ошибка получения данных пользователя: {e}")
        return None
    finally:
        if connect:
            connect.close()


@app.route('/api/user/<user_id>')
def api_get_user_data(user_id):
    user_data = get_user_data(user_id)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({"error": "user not found"}), 404


@app.route('/api/user/update', methods=['POST'])
def api_update_user_data():
    try:
        DB_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../WebTgDB.db"))
        data = request.json
        user_id = data.get('user_id')
        color = data.get('color')
        car = data.get('car')
        connect = sqlite3.connect(DB_PATH)
        cursor = connect.cursor()

        cursor.execute(
            "UPDATE users SET color = ?, car = ? WHERE user_id = ?",
            (color, car, user_id)
        )
        connect.commit()

        return jsonify({"status": "success", "message": "Данные обновлены"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connect:
            connect.close()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
