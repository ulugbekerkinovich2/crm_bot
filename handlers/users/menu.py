from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default.registerKeyBoardButton import menu, application, ask_delete_account
from states.personalData import PersonalData, EducationData
from loader import dp
from utils import send_req
from aiogram import types
from aiogram.dispatcher import FSMContext

@dp.message_handler(Text(equals="🗑Accountni o'chirish"), state=EducationData.menu)
async def delete_account_prompt(message: types.Message, state: FSMContext):
    await message.answer("Account o'chirilsinmi?", reply_markup=ask_delete_account)

@dp.message_handler(Text(equals="Ha, akkauntni o'chirish"), state=EducationData.menu)
async def delete_account(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    delete_account_result = await send_req.delete_profile(token)
    delete_account_result1 = await send_req.delete_profile(token)
    await message.answer(f"Account o'chirildi, {delete_account_result}  {delete_account_result1}", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=EducationData.menu)
async def show_menu(message: Message):
    await message.answer("Akkauntga hush kelibsiz!", reply_markup=menu)
