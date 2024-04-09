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
        f"🇺🇿 <b>Assalomu aleykum, {message.from_user.full_name.capitalize()}!</b>\n"
        f"Bu <i>{university_name_uz}</i> qabul boti. Tilni tanlang.\n\n"
        f"🇷🇺 <b>Здравствуйте, {message.from_user.full_name.capitalize()}!</b>\n"
        f"Это бот приемной комиссии <i>{university_name_ru}</i>. Выберите язык.",
        parse_mode='HTML',
        reply_markup=registerKeyBoardButton.language
    )



    