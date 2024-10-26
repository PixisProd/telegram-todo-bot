from fastapi import FastAPI
from aiogram import types
from config import TELEGRAM_BOT_TOKEN, NGROK_TUNNEL_URL
from bot import bot, dp
from database import create_tables

TELEBOT_URL = f'/bot/{TELEGRAM_BOT_TOKEN}'
NGROK_FULL_URL = f'{NGROK_TUNNEL_URL}{TELEBOT_URL}'

app = FastAPI()

@app.on_event(event_type='startup')
async def on_startup():
    create_tables()
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != NGROK_FULL_URL:
        await bot.set_webhook(NGROK_FULL_URL)

@app.post(TELEBOT_URL)
async def get_updates(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)

@app.on_event(event_type='shutdown')
async def on_shutdown():
    await bot.session.close()