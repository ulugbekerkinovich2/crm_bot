from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from data.config import university_name_uz, university_name_ru
from loader import dp
from states.personalData import PersonalData
from keyboards.default import registerKeyBoardButton
from icecream import ic
from utils import send_req
from data.config import username as USERNAME
from data.config import password as PASSWORD

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    # ic('start tanlandi')
    all_data_state = await state.get_data() 
    token = all_data_state.get('token', None)
    start_count = all_data_state.get('start_count', 0) + 1  
    ic(message)
    date = message.date.strftime("%Y-%m-%d %H:%M:%S")
    ic(date)
    username = message.from_user.username or message.from_user.full_name
    ic(username)
    await state.update_data(start_count=start_count)

    if (start_count > 1 and start_count < 3) or start_count > 8:
        
        username = message.from_user.username or message.from_user.full_name  # Use username if available, otherwise full name
        await message.answer(f"@{username} start tugmasini qayta qayta bosish shart emas😅")

    if start_count > 5 and start_count < 7:
        username = message.from_user.username or message.from_user.full_name
        await message.answer(f"@{username} Iltimos asabiylashmang😅")

    if start_count >= 7 and start_count < 8:
        username_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
        await message.answer(f"{username_display} zerikkan bo'lsangiz\n\nhttps://mentalaba.uz saytini ko'rishni tavsiya qilaman.")
    data_in_state = await state.get_data()
    haveApplicationForm = data_in_state.get('haveApplicationForm', False)
    haveApplied = data_in_state.get('haveApplied', False)
    haveEducation = data_in_state.get('haveEducation', False)
    if token and haveApplicationForm and haveApplied and haveEducation:
        get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
        access = get_djtoken.get('access')
        ic(access)
        await state.update_data(access=access)
        user_chat_id = message.from_user.id
        ic(user_chat_id)
        save_chat_id = send_req.create_user_profile(token=access, chat_id=user_chat_id, 
                                                           first_name=message.from_user.first_name,                                                    last_name=message.from_user.last_name, 
                                                           pin=1)
        ic(save_chat_id)

        get_this_user = send_req.get_user_profile(chat_id=user_chat_id)
        ic(get_this_user)
        # If there's a token, show the main menu
        await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu)
    else:
        # For new users or if there's no token, reset the state and show the welcome message
        await state.finish()
        get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
        access = get_djtoken.get('access')
        ic(access)
        await state.update_data(access=access)
        user_chat_id = message.from_user.id
        ic(user_chat_id)
        save_chat_id = send_req.create_user_profile(token=access, chat_id=user_chat_id, 
                                                           first_name=message.from_user.first_name,                                                    last_name=message.from_user.last_name, 
                                                           pin=1)
        ic(save_chat_id)

        get_this_user = send_req.get_user_profile(chat_id=user_chat_id)
        ic(get_this_user)
        data_user = await state.get_data()
        phone = data_user.get('phone', None)
        ic('user_phone', phone)
        await message.answer(
            f"🇺🇿 <b>Assalomu aleykum, {message.from_user.full_name.capitalize()}!</b>\n"
            f"Bu <i>{university_name_uz}</i> qabul boti. Tilni tanlang.\n\n"
            f"🇷🇺 <b>Здравствуйте, {message.from_user.full_name.capitalize()}!</b>\n"
            f"Это бот приемной комиссии <i>{university_name_ru}</i>. Выберите язык.",
            parse_mode='HTML',
            reply_markup=registerKeyBoardButton.language
        )


