from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic
from aiogram.dispatcher.filters import Command, Text
from keyboards.default.registerKeyBoardButton import update_application
from utils import send_req

@dp.message_handler(Text(equals="📁Arizam"), state="*")
async def menu(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        ic(data)
        await message.answer("Quyidagilardan birini tanlang.", reply_markup=update_application)
    except Exception as e:
        ic(e)
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")

@dp.message_handler(Text(equals="📝Arizani tahrirlash"), state="*")
async def menu(message: types.Message, state: FSMContext):
    try:
        # data = await state.get_data()
        # token = data.get('token')
        # refreshToken = data.get('refreshToken')
        # my_app = await send_req.my_applications(token=token)
        await message.answer("Arizangizni faqat kutilmoqda statusida tahrirlay olasiz", reply_markup=menu)
    except:
        pass