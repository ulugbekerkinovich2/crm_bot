from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default.registerKeyBoardButton import menu, application, update_menu

from loader import dp

@dp.message_handler(Command("application"))
async def show_menu(message: Message):
    await message.answer("Arizalar", reply_markup=application)

@dp.message_handler(text="application")
async def show_application(message: Message):
    await message.answer("Darajani tanlash")


"""
        [
            KeyboardButton(text="Daraja"),
        ],
        [
            KeyboardButton(text="Yo'nalish yoki mutaxassislik"),
        ],
        [
            KeyboardButton(text="Ta'lim shakli"),
        ],
        [
            KeyboardButton(text="O'zbek tili"),
        ]
"""