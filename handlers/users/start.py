from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from data.config import admins_str, university_name_ru, university_name_uz, admin_ids
from loader import dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
# from states.personalData import PersonalData
from keyboards.default import registerKeyBoardButton, adminMenuKeyBoardButton
from icecream import ic
from utils import send_req
from data.config import username as USERNAME
from data.config import password as PASSWORD, BOT_TOKEN
from data.config import university_id as UNIVERSITY_ID
from aiogram.dispatcher.filters import Command, Text

# @dp.message_handler(CommandStart(), state='*')
# async def bot_start(message: types.Message, state: FSMContext):
#     # ic('start tanlandi')
#     all_data_state = await state.get_data() 
#     token = all_data_state.get('token', None)
#     start_count = all_data_state.get('start_count', 0) + 1  
#     ic(message)
#     date = message.date.strftime("%Y-%m-%d %H:%M:%S")
#     ic(date)
#     username = message.from_user.username or message.from_user.full_name
#     ic(username)
#     await state.update_data(start_count=start_count)
#     language_uz = all_data_state.get('language_uz', False)
#     if ((start_count > 1 and start_count < 3) or start_count > 8) and language_uz:
        
#         username = message.from_user.username or message.from_user.full_name  # Use username if available, otherwise full name
#         await message.answer(f"@{username} start tugmasini qayta qayta bosish shart emas😅")
#     data_in_state = await state.get_data()
#     data = await state.get_data()
#     language_uz = data.get('language_uz', None)
#     language_ru = data.get('language_ru', None)
    
#     ic(language_uz, language_ru, 61)
#     if token:
#         user_info = await send_req.application_forms_me(token=token)
#         # ic(user_info)
#         haveApplicationForm = user_info['haveApplicationForm'] if user_info['haveApplicationForm'] else False
#         haveApplied = user_info['haveApplied']
#         haveEducation = user_info['haveEducation']
#         havePreviousEducation = user_info['havePreviousEducation']
#         # ic(haveApplicationForm, haveApplied, haveEducation, havePreviousEducation)

#     if token and haveApplicationForm and haveApplied and (haveEducation or havePreviousEducation):
#         get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
#         access = get_djtoken.get('access')
#         ic(access)
#         await state.update_data(access=access)
#         user_chat_id = message.from_user.id
#         # ic(user_chat_id)
#         try:
#             save_chat_id = send_req.create_user_profile(token=access, chat_id=user_chat_id, 
#                                                             first_name=message.from_user.first_name,
#                                                             last_name=message.from_user.last_name, 
#                                                             pin=1,
#                                                             date=date,
#                                                             username=username,
#                                                             university_name=int(UNIVERSITY_ID)),
        
#             ic(save_chat_id, 70)
#         except Exception as err:
#             ic(err)
#         try:
#             get_this_user = send_req.get_user_profile(chat_id=user_chat_id, university_id=UNIVERSITY_ID)
#             ic(get_this_user, 73)
#         except  Exception as err:
#             ic(err)
#         data = await state.get_data()
#         language_uz = data.get('language_uz', None)
#         language_ru = data.get('language_ru', None)
#         exam_info = await send_req.my_applications(token=token)
#         exam = exam_info.get('exam', {})
#         ic(language_uz, language_ru, 61)
#         check_result = None
#         if exam != {}:
            
#             check_result = exam['exam_result']
#             if language_uz and check_result is None:
#             # If there's a token, show the main menu
#                 await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu)

#         # exam_status = exam_info.get('status')
#         # ic(exam_status, 79)
#         elif exam == {} and language_uz:
#             await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu_full)
#         elif language_uz and check_result is not None:
#             await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu_full)
#         elif language_ru:
#             await message.answer("🏠Меню", reply_markup=registerKeyBoardButton.menu_ru)
#     else:
#         # For new users or if there's no token, reset the state and show the welcome message
#         await state.finish()
#         get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
#         access = get_djtoken.get('access')
#         ic(access)
#         await state.update_data(access=access)
#         user_chat_id = message.from_user.id
#         ic(user_chat_id)
#         save_chat_id = send_req.create_user_profile(token=access, 
#                                                     chat_id=user_chat_id, 
#                                                     first_name=message.from_user.first_name,                                                    
#                                                     last_name=message.from_user.last_name, 
#                                                     pin=1,
#                                                     date=date,
#                                                     username=username,
#                                                     university_name=int(UNIVERSITY_ID)),
        
#         ic(72, save_chat_id)

#         get_this_user = send_req.get_user_profile(chat_id=user_chat_id, university_id=UNIVERSITY_ID)
#         ic(get_this_user)
#         data_user = await state.get_data()
#         phone = data_user.get('phone', None)
#         ic('user_phone', phone)
#         await message.answer(
#             f"🇺🇿 <b>Assalomu aleykum, {message.from_user.full_name.capitalize()}!</b>\n"
#             f"Bu <i>{university_name_uz}</i> qabul boti. Tilni tanlang.\n\n"
#             f"🇷🇺 <b>Здравствуйте, {message.from_user.full_name.capitalize()}!</b>\n"
#             f"Это бот приемной комиссии <i>{university_name_ru}</i>. Выберите язык.",
#             parse_mode='HTML',
#             reply_markup=registerKeyBoardButton.language
#         )
# @dp.message_handler(CommandStart(), state='*')
# async def bot_start(message: types.Message, state: FSMContext):
#     ic('started...')
#     all_data_state = await state.get_data()
#     token = all_data_state.get('token', None)
#     start_count = all_data_state.get('start_count', 0) + 1
#     date = message.date.strftime("%Y-%m-%d %H:%M:%S")
#     username = message.from_user.username or message.from_user.full_name
#     await state.update_data(start_count=start_count)
#     language_uz = all_data_state.get('language_uz', False)

#     if (1 < start_count < 3 or start_count > 8) and language_uz:
#         await message.answer(f"@{username} start tugmasini qayta qayta bosish shart emas😅")
#         return
#     ic(140, token)
#     if token:
#         user_info = await send_req.application_forms_me(token=token)
#         have_application_form = user_info.get('haveApplicationForm', False)
#         have_applied = user_info.get('haveApplied', False)
#         have_education = user_info.get('haveEducation', False)
#         have_previous_education = user_info.get('havePreviousEducation', False)

#         if have_application_form and have_applied and (have_education or have_previous_education):
#             await handle_authenticated_user(message, state, token, date, username)
#         else:
#             await handle_new_user(message, state, date, username)
#     else:
#         await handle_new_user(message, state, date, username)
@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    ic('started...')
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    username = message.from_user.username or message.from_user.full_name
    chat_id = message.from_user.id
    date = message.date.strftime("%Y-%m-%d %H:%M:%S")

    # Foydalanuvchilar va botlar ro‘yxatini olish
    all_bots = send_req.get_all_bots()
    all_users = send_req.get_all_users()
    ic(all_users)
    ic(all_bots)
    if chat_id in admin_ids:
        await message.answer(f"Admin Reklama paneliga xush kelibsiz, {message.from_user.full_name}!", reply_markup=adminMenuKeyBoardButton.adminMenu)
        return
    elif chat_id not in all_users:
        ic('user not found, saving...')
        for bot in all_bots:
            if bot["api_key"] == BOT_TOKEN:
                bot_id = bot["id"]
                ic('matched bot, saving user...')
                # send_req.save_chat_id(chat_id, firstname, lastname, bot_id, username, 'active')
                
        # await message.answer(f"Salom, {message.from_user.full_name}! {chat_id}")
    else:
        await message.answer(f"Siz ro'yxatdan o'tgansiz, {message.from_user.full_name}!")

    # FSM holatini olish va yangilash
    all_data_state = await state.get_data()
    token = all_data_state.get('token', None)
    start_count = all_data_state.get('start_count', 0) + 1
    language_uz = all_data_state.get('language_uz', False)
    await state.update_data(start_count=start_count)

    # Agar start tugmasini juda ko‘p bosgan bo‘lsa
    if (1 < start_count < 3 or start_count > 8) and language_uz:
        await message.answer(f"@{username} start tugmasini qayta qayta bosish shart emas😅")
        return

    ic(140, token)
    if token:
        user_info = await send_req.application_forms_me(token=token)
        have_application_form = user_info.get('haveApplicationForm', False)
        have_applied = user_info.get('haveApplied', False)
        have_education = user_info.get('haveEducation', False)
        have_previous_education = user_info.get('havePreviousEducation', False)

        if have_application_form and have_applied and (have_education or have_previous_education):
            await handle_authenticated_user(message, state, token, date, username)
        else:
            await handle_new_user(message, state, date, username)
    else:
        await handle_new_user(message, state, date, username)



async def handle_authenticated_user(message, state, token, date, username):
    get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
    access = get_djtoken.get('access')
    await state.update_data(access=access)
    user_chat_id = message.from_user.id

    try:
        await send_req.create_user_profile(
            token=access,
            chat_id=user_chat_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            pin=1,
            date=date,
            username=username,
            university_name=int(UNIVERSITY_ID)
        )
    except Exception as err:
        ic(err)

    try:
        get_this_user = send_req.get_user_profile(chat_id=user_chat_id, university_id=UNIVERSITY_ID)
        ic(get_this_user)
    except Exception as err:
        ic(err)

    exam_info = await send_req.my_applications(token=token)
    exam = exam_info.get('exam', {})
    check_result = exam.get('exam_result', None)

    data = await state.get_data()
    language_uz = data.get('language_uz', None)
    language_ru = data.get('language_ru', None)

    if language_uz:
        if check_result is None:
            await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu)
        else:
            await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.menu_full)
    elif language_ru:
        await message.answer("🏠Меню", reply_markup=registerKeyBoardButton.menu_ru)


async def handle_new_user(message, state, date, username):
    ic('handle_new_user')
    await state.finish()
    get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
    access = get_djtoken.get('access')
    ic(204, access)
    await state.update_data(access=access)
    user_chat_id = message.from_user.id

    await send_req.create_user_profile(
        token=access,
        chat_id=user_chat_id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        pin=1,
        date=date,
        username=username,
        university_name=int(UNIVERSITY_ID)
    )

    get_this_user = send_req.get_user_profile(chat_id=user_chat_id, university_id=UNIVERSITY_ID)
    data_user = await state.get_data()
    phone = data_user.get('phone', None)

    await message.answer(
        f"🇺🇿 <b>Assalomu aleykum, {message.from_user.full_name.capitalize()}!</b>\n"
        f"Bu <i>{university_name_uz}</i> qabul boti. Tilni tanlang.\n\n"
        f"🇷🇺 <b>Здравствуйте, {message.from_user.full_name.capitalize()}!</b>\n"
        f"Это бот приемной комиссии <i>{university_name_ru}</i>. Выберите язык.",
        parse_mode='HTML',
        reply_markup=registerKeyBoardButton.language
    )
@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await handle_start(message, state)

async def handle_start(message: types.Message, state: FSMContext):
    start_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    ).add(KeyboardButton('/start'))

    await message.answer("Bot ishga tushdi", reply_markup=start_keyboard)
    await state.finish()

@dp.message_handler(Text(equals='/restart'), state='*')
async def bot_restart(message: types.Message, state: FSMContext):
    # await message.answer("Bot qayta ishga tushdi")
    await state.finish()
    await handle_start(message, state)




@dp.message_handler(Text(equals='/admin'), state='*')
async def admin_command(message: types.Message):
    await message.answer("Assalomu alaykum,\n\n"
"Qo'llab-quvvatlash xizmati boti orqali texnik yordam va hujjat topshirishda yordam olishingiz mumkin. Qo\'shimcha ma\'lumot uchun administratorga murojaat qiling: <a href='https://t.me/universittet_qabul_admin_bot'>Admin</a>"
, parse_mode='HTML')
    

# @dp.message_handler(state='*')
# async def default_message_handler(message: types.Message, state: FSMContext):
#     await state.finish()
#     await handle_start(message, state)
