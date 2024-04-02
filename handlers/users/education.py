import logging
from keyboards.inline.menukeyboards import coursesMenu,categoryMenu
# from keyboards.default.registerKeyBoardButton import 
from loader import dp
from aiogram.types import Message, CallbackQuery


@dp.message_handler(text_contains='directions')
async def select_directions(message: Message):
    await message.answer(f"Yonalish tanla", reply_markup=categoryMenu)

@dp.callback_query_handler(text='courses')
async def courses(call: CallbackQuery):
    await call.message.asnwer("yonalish tanla", reply_markup=coursesMenu)
    await call.answer(cache_time=20)