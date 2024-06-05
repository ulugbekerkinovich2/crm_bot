from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from data.config import university_name_uz, university_name_ru
from loader import dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
# from states.personalData import PersonalData
from keyboards.default import registerKeyBoardButton
from icecream import ic
from utils import send_req
from data.config import username as USERNAME
from data.config import password as PASSWORD
from aiogram.dispatcher.filters import Command, Text
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
    language_uz = all_data_state.get('language_uz', False)
    if ((start_count > 1 and start_count < 3) or start_count > 8) and language_uz:
        
        username = message.from_user.username or message.from_user.full_name  # Use username if available, otherwise full name
        await message.answer(f"@{username} start tugmasini qayta qayta bosish shart emas😅")

    # if start_count > 5 and start_count < 7:
    #     username = message.from_user.username or message.from_user.full_name
    #     await message.answer(f"@{username} Iltimos asabiylashmang😅")

    # if start_count >= 7 and start_count < 8:
    #     username_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    #     await message.answer(f"{username_display} zerikkan bo'lsangiz\n\nhttps://mentalaba.uz saytini ko'rishni tavsiya qilaman.")
    data_in_state = await state.get_data()
    # haveApplicationForm = data_in_state.get('haveApplicationForm', False)
    # haveApplied = data_in_state.get('haveApplied', False)
    # haveEducation = data_in_state.get('haveEducation', False)
    # havePreviousEducation = data_in_state.get('havePreviousEducation', False)
    data = await state.get_data()
    language_uz = data.get('language_uz', None)
    language_ru = data.get('language_ru', None)
    
    ic(language_uz, language_ru, 61)
    if token:
        user_info = await send_req.application_forms_me(token=token)
        # ic(user_info)
        haveApplicationForm = user_info['haveApplicationForm'] if user_info['haveApplicationForm'] else False
        haveApplied = user_info['haveApplied']
        haveEducation = user_info['haveEducation']
        havePreviousEducation = user_info['havePreviousEducation']
        # ic(haveApplicationForm, haveApplied, haveEducation, havePreviousEducation)

    if token and haveApplicationForm and haveApplied and (haveEducation or havePreviousEducation):
        get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
        access = get_djtoken.get('access')
        ic(access)
        await state.update_data(access=access)
        user_chat_id = message.from_user.id
        # ic(user_chat_id)
        try:
            save_chat_id = send_req.create_user_profile(token=access, chat_id=user_chat_id, 
                                                            first_name=message.from_user.first_name,
                                                            last_name=message.from_user.last_name, 
                                                            pin=1,
                                                            date=date,
                                                            username=username),
        
            ic(save_chat_id, 70)
        except Exception as err:
            ic(err)
        get_this_user = send_req.get_user_profile(chat_id=user_chat_id)
        ic(get_this_user, 73)
        data = await state.get_data()
        language_uz = data.get('language_uz', None)
        language_ru = data.get('language_ru', None)
        exam_info = await send_req.my_applications(token=token)
        exam = exam_info.get('exam', {})
        ic(language_uz, language_ru, 61)
        check_result = None
        if exam != {}:
            
            check_result = exam['exam_result']
            if language_uz and check_result is None:
            # If there's a token, show the main menu
                await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu)

        # exam_status = exam_info.get('status')
        # ic(exam_status, 79)
        elif exam == {} and language_uz:
            await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu_full)
        elif language_uz and check_result is not None:
            await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu_full)
        elif language_ru:
            await message.answer("🏠Меню", reply_markup=registerKeyBoardButton.menu_ru)
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
                                                           pin=1,
                                                           date=date,
                                                           username=username),
        ic(72, save_chat_id)

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


@dp.message_handler(Text(equals='/restart'), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    start_button = KeyboardButton('/start')  # The text on the button
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)
    await message.answer("Bot qayta ishga tushdi",reply_markup=start_keyboard)
    await state.finish()