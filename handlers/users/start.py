from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from data.config import university_name_uz, university_name_ru
from loader import dp
from states.personalData import PersonalData
from keyboards.default import registerKeyBoardButton

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    # Reset state
    await state.finish()
    
    # Your welcome message
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(
        f"🇺🇿Assalomu aleykum {message.from_user.full_name.capitalize()} bu <b>{university_name_uz}</b> qabul boti tilni\n\n🇷🇺Здравствуйте, {message.from_user.full_name.capitalize()}, это бот приемной комиссии <b>{university_name_ru}</b>, выберите язык",
        parse_mode='HTML',
        reply_markup=registerKeyBoardButton.language
    )


    