from aiogram.fsm.state import StatesGroup, State


class EditState(StatesGroup):
    waiting_username = State()


class AddState(StatesGroup):
    collecting = State()
