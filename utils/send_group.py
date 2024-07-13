import requests
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
from data.config import GROUP_CHAT_ID
from loader import dp, bot
from icecream import ic


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher


dp.middleware.setup(LoggingMiddleware())

async def send_group(message):
    try:
        formatted_message = "```\n" + json.dumps(message, indent=4) + "\n```"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=formatted_message, parse_mode="Markdown")
    except Exception as e:
        ic(e)
        pass