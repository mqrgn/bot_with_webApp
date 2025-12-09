import aiosqlite
from aiogram import types

import os
import uuid


def generate_uuid_token():
    return str(uuid.uuid4())


DB_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../WebTgDB.db"))


async def add_user(user_id):
    token = generate_uuid_token()
    connect = await aiosqlite.connect(DB_PATH)
    cursor = await connect.cursor()
    user = await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = await user.fetchone()
    if not user:
        await cursor.execute(
            'INSERT INTO users (user_id, color, car) VALUES (?, ?, ?)', (user_id, "unknown", "unknown")
        )
        await connect.commit()
    await cursor.close()
    await connect.close()


async def set_user_color(user_id, color):
    connect = await aiosqlite.connect(DB_PATH)
    cursor = await connect.cursor()
    await cursor.execute(
        'UPDATE users SET color = ? WHERE user_id = ?', (color, user_id,)
    )
    await connect.commit()
    await cursor.close()
    await connect.close()


async def set_user_car(user_id, car):
    connect = await aiosqlite.connect(DB_PATH)
    cursor = await connect.cursor()
    await cursor.execute(
        'UPDATE users SET car = ? WHERE user_id = ?', (car, user_id,)
    )
    await connect.commit()
    await cursor.close()
    await connect.close()






