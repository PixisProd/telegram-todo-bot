from aiogram.fsm.state import StatesGroup, State

class TaskCreation(StatesGroup):
    task_name = State()
    query_handle = State()

class TaskDeletion(StatesGroup):
    task_id = State()

class TaskEditing(StatesGroup):
    task_id = State()
    query_handle = State()