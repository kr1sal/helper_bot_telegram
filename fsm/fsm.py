from aiogram.fsm.state import StatesGroup, State


class FSM(StatesGroup):
    change_language_state = State()
    get_city_state = State()
    get_qr_code_state = State()
