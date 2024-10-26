from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

class SetStatusForTask(CallbackData, prefix='my'):
    status: str

def get_start_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="📋 Task list")
    kb.button(text="➕ Add task")
    kb.button(text="🗑️ Delete task")
    kb.button(text="🔄 Edit task")
    kb.adjust(2, 2)
    return kb.as_markup()

def get_status_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="✔️ Done", callback_data=SetStatusForTask(status='✔️ Done'))
    kb.button(text="⏳ Pending", callback_data=SetStatusForTask(status='⏳ Pending'))
    kb.button(text="⏲️ In process", callback_data=SetStatusForTask(status='⏲️ In process'))
    return kb.as_markup()