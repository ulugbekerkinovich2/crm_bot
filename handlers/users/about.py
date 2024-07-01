from loader import dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from data.config import web_app_url

@dp.message_handler(commands=['about', 'Открыть страницу университета', 'Universitet sahifasini ochish'])
async def send_about_info(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton(
        text="Universitet haqida",
        web_app=types.WebAppInfo(url=web_app_url)
    )
    keyboard.add(web_app_button)
    message_text = """
    *Universitet haqida bilish uchun quyidagi tugmani bosing*

    Нажмите кнопку ниже, чтобы узнать об университете:
    """
    await message.reply(message_text, reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)