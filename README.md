# To-Do Bot

A powerful and efficient To-Do bot built using [Aiogram 3](https://docs.aiogram.dev/en/latest/) for Telegram and [FastAPI](https://fastapi.tiangolo.com/) as the server, utilizing [SQLite](https://sqlite.org/) for data storage. This bot is optimized for key functionalities such as task creation, editing, and management.

## Features

- **Task Creation**: Easily add new tasks to your list.
- **Task Management**: Edit and update task statuses seamlessly.
- **Logging**: Track task creation and update dates separately for better organization.
- **Modular Design**: The code is organized into well-structured modules for ease of use and maintenance.

## Instalation

1. **First, select the location where you want to install the bot:**
```bash
cd <your-repository-folder>
```
2. **Next, clone the repository:**
```bash
git clone https://github.com/PixisProd/telegram-todo-bot.git
```
3. **After which you can optionally create a virtual environment, this is not necessary, but I would recommend:**
```bash
python -m venv .env
```
4. **Next you need to install the dependencies:**
```bash
pip install -r requirements.txt
```
5. **In order for Telegram to see our fastapi server on the local machine, you need to use [ngrok](https://ngrok.com/download).**

## Preparation

1. Create a telegram bot using [BotFather](https://telegram.me/BotFather) and get your bot token, or if you already have a bot, then take an existing one.

2. Then find the `config.py` file in the project and paste your bot's token into the `TELEGRAM_BOT_TOKEN` field.

3. **Open `ngrok.exe` and enter the following command:**
```bash
ngrok http <your-port>
```
4. After you see that in ngrok `Session status` is `online` and lights up green, then the tunnel is ready to work through the port you selected. **Be sure to remember the port you specified.**

5. In the left column you need to find the `Forwarding` field and copy the url that ends with `.ngrok-free.app`.

6. Open the `config.py` file and paste the url we got in the paragraph above into the `NGROK_TUNNEL_URL` field.

## Bot startup

After all these preparations, we can finally start working with our bot.

1. **Activate your virtual environment:**
```bash
<directory>/.env/Scripts/activate
```
Here `.env` is the name of your virtual environment, if you changed it when creating it, then replace `.env` with the name of your environment

2. **Start FastAPI server:**
```bash
uvicorn main:app --host 0.0.0.0 --port <your-port>
```
Here `your-port` is the port you specified when creating the tunnel to ngrok.

After all this, your bot is ready to work.

## Conclusion

Feel free to contribute to the project by reporting issues, suggesting features, or submitting pull requests. Your feedback and contributions are always welcome!

_Happy task management! 🎉_
