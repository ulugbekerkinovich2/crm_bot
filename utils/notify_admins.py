import logging

from aiogram import Dispatcher

from data.config import ADMINS
from datetime import datetime

async def on_startup_notify(dp: Dispatcher):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, f"CRM bot ishga tushdi {start_time}")

        except Exception as err:
            logging.exception(err)
