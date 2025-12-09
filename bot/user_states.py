from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    color = State()
    car = State()