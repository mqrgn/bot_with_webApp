import os

import aiosqlite
from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from user_states import UserState

DB_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../WebTgDB.db"))


async def get_info_callback(callback: types.CallbackQuery) -> None:
    user_id = callback.from_user.id
    connect = await aiosqlite.connect(DB_PATH)
    cursor = await connect.cursor()
    info = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    info = await info.fetchone()
    user_id, color, car = info
    message_text = f"📊 Ваша информация:\n\n👤 ID: {user_id}\n🎨 Цвет: {color}\n🚗 Авто: {car}"
    await cursor.close()
    await connect.close()

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
    ])

    await callback.message.edit_text(message_text, reply_markup=kb)


async def menu_callback(callback: types.CallbackQuery) -> None:
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Посмотреть информацию о себе", callback_data="get_info")],
                         [types.InlineKeyboardButton(text="Изменить цвет", callback_data="set_color")],
                         [types.InlineKeyboardButton(text="Марка авто", callback_data="set_car")],
                         ])
    await callback.message.edit_text(f"Здарова братанчик, я запоминаю информацию, "
                                     f"\nкоторую ты мне введешь", reply_markup=kb)


async def set_color_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data='menu')]
    ])
    await state.set_state(UserState.color)
    await callback.message.edit_text("Напиши цвет, который я отображу в информации о тебе: ", reply_markup=kb)


async def set_car_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Назад", callback_data='menu')]
    ])
    await state.set_state(UserState.car)
    await callback.message.edit_text("Напиши авто, которое я отображу в информации о тебе: ", reply_markup=kb)


def register_callback_handlers(dp: Dispatcher) -> None:
    dp.callback_query.register(get_info_callback, F.data == 'get_info')
    dp.callback_query.register(menu_callback, F.data == 'menu')
    dp.callback_query.register(set_color_callback, F.data == 'set_color')
    dp.callback_query.register(set_car_callback, F.data == 'set_car')
