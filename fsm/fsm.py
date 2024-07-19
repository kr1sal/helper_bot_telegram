from aiogram.fsm.state import StatesGroup, State


class FSM(StatesGroup):
    change_language = State()
    get_city = State()
