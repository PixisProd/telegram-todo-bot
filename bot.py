from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from datetime import datetime
from keyboards import get_start_keyboard, get_status_keyboard, SetStatusForTask
from database import add_user, add_task, get_task_list, delete_task_by_id, edit_task_by_id, get_task_by_id
from FSM_states_group import TaskCreation, TaskDeletion, TaskEditing
from config import TELEGRAM_BOT_TOKEN

# Bot and dispatcher creation
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


# Start handler
@dp.message(CommandStart())
async def start(message: types.Message):
    add_user(user_id=message.from_user.id)
    greeting_message = """
    <b>Hey there!</b> 😊 I'm your To-Do bot! Here’s what I can do for you:
        - 📝 Save tasks
        - 🔄 Manage yout tasks
        - 📅 Track actions related to tasks
    Let’s get started! 🚀
    """
    greeting_photo = types.FSInputFile(path='img\\greeting.jpg')
    await message.answer_photo(photo=greeting_photo, caption=greeting_message, parse_mode='HTML', reply_markup=get_start_keyboard())


# Task list
@dp.message(F.text == '📋 Task list')
async def add_task_handler(message: types.Message):
    users_tasks = get_task_list(user_id=message.from_user.id)
    strforanswer = ""
    for item in users_tasks:
        strforanswer += f"🗂️ <b>Task ID:</b> {item[0]}\n📝 <b>Name:</b> {item[2].capitalize()}\n📅 <b>Status:</b> {item[3]}\n<b>🕒 Created at:</b> <i>{item[4]}</i>\n<b>🔄 Last update:</b> <i>{item[5]}</i>\n────────────\n"
    if strforanswer == "":
        await message.answer(text="You don't have any tasks")
    else:
        await message.answer(text=strforanswer, parse_mode='HTML')


# Add task
@dp.message(F.text == '➕ Add task')
async def start_task_registration(message: types.Message, state: FSMContext):
    await message.reply(text="Enter your task name: ")
    await state.set_state(TaskCreation.task_name)

@dp.message(TaskCreation.task_name)
async def process_task_name(message: types.Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    await state.update_data(user_id=message.from_user.id)
    await message.answer(text="Choose status for your task:", reply_markup=get_status_keyboard())
    await state.set_state(TaskCreation.query_handle)

@dp.callback_query(SetStatusForTask.filter(), TaskCreation.query_handle)
async def process_query_handle(query: types.callback_query.CallbackQuery, callback_data: SetStatusForTask, state: FSMContext):
    user_data = await state.get_data()
    task_name = user_data['task_name']
    status = callback_data.status
    user_id = user_data['user_id']
    creation_time = datetime.now().strftime(r'%d-%m-%Y %H:%M')
    add_task(user_id=user_id, task_name=task_name, status=status, creation_time=creation_time, last_update=creation_time)
    await query.message.answer(text=f"Task \"{task_name}\" created with status: {status}")
    await query.message.delete()
    await query.answer()
    await state.clear()


# Delete task
@dp.message(F.text == "🗑️ Delete task")
async def delete_task(message: types.Message, state: FSMContext):
    await message.reply(text="Enter task ID to delete")
    await state.set_state(TaskDeletion.task_id)

@dp.message(TaskDeletion.task_id)
async def process_deletion(message: types.Message, state: FSMContext):
    task_id = message.text
    is_task_deleted = delete_task_by_id(task_id=task_id, user_id=message.from_user.id)
    if not is_task_deleted:
        await message.reply(f"There are no tasks with ID: {task_id}")
    else:
        await message.reply("Task successfully deleted")
    await state.clear()


# Edit task
@dp.message(F.text == "🔄 Edit task")
async def edit_task(message: types.Message, state: FSMContext):
    await message.reply(text="Enter task ID to edit")
    await state.set_state(TaskEditing.task_id)

@dp.message(TaskEditing.task_id)
async def task_editing_get_task_id(message: types.Message, state: FSMContext):
    await state.update_data(task_id=message.text)
    await state.update_data(user_id=message.from_user.id)
    is_task_found = get_task_by_id(task_id=message.text, user_id=message.from_user.id)
    if is_task_found != None:
        await message.reply(text="Choose new status for your task:", reply_markup=get_status_keyboard())
        await state.set_state(TaskEditing.query_handle)
    else:
        await message.reply(text=f"There are no tasks with ID: {message.text}")
        await state.clear()


@dp.callback_query(SetStatusForTask.filter(), TaskEditing.query_handle)
async def task_editing_get_task_status(query: types.callback_query.CallbackQuery, callback_data: SetStatusForTask, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    task_id = data["task_id"]
    task_info = get_task_by_id(task_id=task_id, user_id=user_id)
    new_status = callback_data.status
    update_time = datetime.now().strftime(r'%d-%m-%Y %H:%M')
    edit_task_by_id(task_id=task_id, user_id=user_id, new_status=new_status, update_time=update_time)
    await query.message.answer(text=f"Task \"{task_info[0]}\" now have new status: {new_status}")
    await query.message.delete()
    await query.answer()
    await state.clear()
    

# Echo
@dp.message()
async def echo(message: types.Message):
    await message.answer(text=f"{message.text}")