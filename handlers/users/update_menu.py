from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default.registerKeyBoardButton import menu, application, update_menu

from loader import dp

@dp.message_handler(Command("update_menu"))
async def show_menu(message: Message):
    await message.answer("Ma'lumolarni tahrirlash", reply_markup=update_menu)

@dp.message_handler(text="Shaxsiy ma'lumotlarni tahrirlash")
async def update_personal_data(message: Message):
    await message.answer("Shaxsiy ma'lumotlarni tahrirlash dasturlanmoqda", reply_markup=update_menu)


@dp.message_handler(text="Ta'lim ma'lumotlarini tahrirlash")
async def update_personal_data(message: Message):
    await message.answer("Ta'lim ma'lumotlarini tahrirlash dasturlanmoqda", reply_markup=update_menu)

@dp.message_handler(text="Chet tili sertifikatini tahrirlash")
async def update_personal_data(message: Message):
    await message.answer("Chet tili sertifikatini tahrirlash dasturlanmoqda", reply_markup=update_menu)

@dp.message_handler(text="Arizani tahrirlash")
async def update_personal_data(message: Message):
    await message.answer("Arizani tahrirlash dasturlanmoqda", reply_markup=update_menu)

