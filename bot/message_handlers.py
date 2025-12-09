from aiogram import Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from functions_db import add_user, set_user_color, set_user_car
from user_states import UserState


async def start_command(message: types.Message) -> None:
    await add_user(message.from_user.id)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Посмотреть информацию о себе", callback_data="get_info")],
                         [types.InlineKeyboardButton(text="Изменить цвет", callback_data="set_color")],
                         [types.InlineKeyboardButton(text="Марка авто", callback_data="set_car")],
                         ])
    await message.answer(f"Здарова братанчик, я запоминаю информацию, \nкоторую ты мне введешь", reply_markup=kb)


async def set_color_handler(message: types.Message, state: FSMContext) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='В меню', callback_data='menu')]
    ])

    color = message.text

    await set_user_color(message.from_user.id, color)
    await message.answer("Цвет успешно изменен!", reply_markup=kb)
    await state.set_state(state=None)


async def set_car_handler(message: types.Message, state: FSMContext) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='В меню', callback_data='menu')]
    ])

    car = message.text

    await set_user_car(message.from_user.id, car)
    await message.answer("Машина успешно изменена!", reply_markup=kb)
    await state.set_state(state=None)


def register_message_handlers(dp: Dispatcher) -> None:
    dp.message.register(start_command, CommandStart())
    dp.message.register(set_color_handler, UserState.color)
    dp.message.register(set_car_handler, UserState.car)
