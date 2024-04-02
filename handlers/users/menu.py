from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default.registerKeyBoardButton import menu, application, update_menu

from loader import dp

@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Shaxsiy ma'lumotlar", reply_markup=menu)