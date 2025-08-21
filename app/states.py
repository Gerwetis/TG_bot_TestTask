from aiogram.fsm.state import StatesGroup, State

class AuthStates(StatesGroup):
    waiting_for_key = State()

class UploadStates(StatesGroup):
    waiting_for_file = State()
