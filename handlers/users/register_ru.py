from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command,Text
from utils import send_req
from loader import dp
from states.personalData import PersonalDataRU, EducationDataRU
from states.personalData import ManualPersonalInfoRU
from aiogram.utils.exceptions import Throttled
from data.config import throttling_time, domain_name
from pprint import pprint
from datetime import datetime
from handlers.users import collect_data, upload
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
import os
import aiofiles.os
from icecream import ic
import json
from keyboards.default.registerKeyBoardButton import yes_no,update_education_info,yes_no_ru,update_education_info_ru
from keyboards.default.registerKeyBoardButton import enter_button, menu,register,register_ru,menu_ru,enter_button_ru
from data.config import username as USERNAME
from data.config import password as PASSWORD
from data.config import university_id as UNIVERSITY_ID

# saved_message = "✅ <b>Ma'lumot saqlandi!</b>"
saved_message_ru = "✅ <b>Данные сохранены!</b>"
# error_message_birthday = "🔴 Tug'ilgan kun noto'g'ri kiritildi. Sana formati: yyyy-oo-kk\nTug'ilgan kunni qayta kiriting"
error_message_birthday_ru = "🔴Дата рождения указана неверно. Формат даты: гггг-мм-дд\nПовторно введите дату рождения."
# error_date = "🔴 Tug'ilgan kun noto'g'ri kiritildi. Kiritilgan sana namunadagidek emas.\nTug'ilgan kunni qayta kiriting"
error_date_ru = "🔴Дата рождения указана неверно. Введенная дата не совпадает с приведенной в примере.\nПовторно введите дату рождения."
# example_birthday = "Tug\'ilgan kuningingizni kiriting quidagi formatda\nyyyy-oo-kk\n\nNamuna: 2005-03-21"
example_birthday_ru = "Введите дату рождения в следующем формате\nгггг-мм-дд-\n\nПример: 2005-03-21."
# example_phone = "☎️ <b>Telefon raqamingizni yuboring</b>\n<i>Namuna: 998991234567</i>"
example_phone_ru = "☎️ <b>Отправьте свой номер телефона</b>\n<i>Пример: 998991234567</i>"
# example_extra_phone = 'Siz bilan aloqaga chiqish uchun qo\'shimcha telefon raqam kiriting\n\nNamuna: +998991234567'
example_extra_phone_ru = "Введите дополнительный номер телефона, чтобы связаться с вами.\n\nПример: +998991234567"
# example_transkript_message = "✅ *Transkript nusxasini yuboring* \n(_Hajmi 5 MB dan katta bo'lmagan, .png, .jpg, .jpeg, .pdf faylni yuklang_"
example_transkript_message_ru = "✅ *Отправьте копию стенограммы* \n(_Загрузите файл .png, .jpg, .jpeg, .pdf размером не более 5 МБ_"
# example_diploma_message = "✅ *Diplom, shahodatnoma yoki ma’lumotnoma nusxasini yuboring* \n(_Hajmi 5 MB dan katta bo'lmagan, .png, .jpg, .jpeg, .pdf fayllarni yuklang_"
example_diploma_message_ru = "✅ *Отправьте копию диплома, сертификата или справки* \n(_Загрузить файлы .png, .jpg, .jpeg, .pdf размером не более 5 МБ_"
# example_certification_message = "✅ *Chet tili sertifikat nusxasini yuboring* \n(_Hajmi 5 MB dan katta bo'lmagan, .png, .jpg, .jpeg, .pdf fayllarni yuklang_"
example_certification_message_ru = "✅ *Отправьте копию сертификата по иностранному языку* \n(_Загрузить файлы .png, .jpg, .jpeg, .pdf размером не более 5 МБ_"
# accepted_phone = "🟢 <b>Telefon raqamingiz qabul qilindi.</b> Telefon raqamingizga yuborilgan kodni kiriting"
accepted_phone_ru = "🟢 <b>Ваш номер телефона принят.</b> Введите код, отправленный на ваш номер телефона."
# accepted_birthday_saved_data = '🟢Tu\'gilgan kuningiz qabul qilindi. Ma\'lumotlaringiz muvaffaqiyatli saqlandi.'
accepted_birthday_saved_data_ru = "🟢Ваш день рождения принят. Ваши данные успешно сохранены."
# error_message_phone = "🔴Telefon raqam no\'to\'g\'ri kiritildi, Namunadagidek raqam kiriting!"
error_message_phone_ru = "🔴Номер телефона введен неверно, пожалуйста, введите номер по образцу!"
# accepted_phone_simple = "🟢Telefon raqamingiz qabul qilindi."
accepted_phone_simple_ru = "🟢Ваш номер телефона принят."
# accepted_document = "🟢Passport seriyasi qabul qilindi"
accepted_document_ru = "🟢Принимаются серии паспортов"
# example_document = "Passport seriyangizni yuboring\nNamuna: AB1234567"
example_document_ru = "Отправьте серийный номер паспорта\nОбразец: AB1234567"
# error_document = "🔴Passport seriya noto'g'ri kiritildi"
error_document_ru = "🔴Неверно указана серия паспорта"
# error_secret_code = "🔴Tasdiqlash kodi noto'g'ri kiritildi"
error_secret_code_ru = "🔴Код подтверждения введен неверно"
# error_type_edu_name = 'Talim dargoh nomini kiriting, bu majburiy.\nNamuna: 12-maktab'
error_type_edu_name_ru = 'Talim dargoh nomini kiriting, bu majburiy.\nNamuna: 12-maktab'
# error_document = "Passport seriyasi 2 ta harfdan  va 7 raqamdan iborat bo'lishi kerak.\nQayta passport seriyangizni kiriting"
error_document_ru = "Серия паспорта должна содержать 2 буквы и 7 цифр.\nПовторно введите серию паспорта."
# select_region = "Ta'lim dargohi joylashgan shahar yoki viloyatni tanlang:"
select_region_ru = "Выберите город или регион, где расположен образовательный центр:"
# select_degree = "<b>*Daraja tanlang:</b>"
select_degree_ru = "<b>*Выберите уровень:</b>"
# select_direction = "Yo'nalish yoki mutaxassislikni tanlang:"
select_direction_ru = "Выберите сферу или специализацию:"
# select_edu_type = "Ta'lim shaklini tanglang:"
select_edu_type_ru = "Выберите тип образования:"
# select_edu_language = "Ta'lim tilini tanlang:"
select_edu_language_ru = "Выберите язык обучения:"
# select_type_certificate = "Sertifikat turini tanlang:"
select_type_certificate_ru = "Выберите тип сертификата:"
# select_country = "Ta’lim dargohi joylashgan davlatni tanlang:"
select_country_ru = "Выберите страну, в которой находится учебное заведение:"
# type_your_edu_name = "Ta'lim dargohi nomini kiriting:\nNamuna: 12-maktab"
type_your_edu_name_ru = "Введите название школы:\nПример: 12-я школа."
# wait_file_is_loading = "<b>Kuting, fayl yuklanmoqda.</b>"
wait_file_is_loading_ru = "<b>Подождите, файл загружается.</b>"
# retype_secret_code = "Tasdiqlash kodini qayta kiriting"
retype_secret_code_ru = "Повторно введите код подтверждения"
# application_submited = 'Ariza muvaffaqiyatli topshirildi'
application_submited_ru = 'Заявка успешно отправлена'
# server_error = '🔴Ma\'lumotlaringizni markaziy ma\'lumotlar omboridan topolmadim\nMa\'lumotlaringizni kiritishingiz mumkin.'
server_error_ru = '🔴Мне не удалось найти вашу информацию в центральной базе данных.\nВы можете ввести свою информацию.'
# error_pin = "🔴 JSHSHR 14 raqamdan iborat bolishi kerak"
error_pin_ru = "🔴 ПИНФЛ должен состоять из 14 цифр."
# error_number = "🔴 Telefon nomer 9ta raqamdan iborat bo'lishi kerak, Iltimos namunadagidek raqam kiriting"
error_number_ru = "🔴 Telefon nomer 9ta raqamdan iborat bo'lishi kerak, Iltimos namunadagidek raqam kiriting"
# error_birthplace = "🔴 Tug'ilgan joy noto'g'ri kiritildi"
error_birthplace_ru = "🔴 Место рождения указано неверно"
# search_university = "Mamlakat qisqa nomi yoki to'liq nomini kiriting: Namuna Amerika"
search_university_ru = "Введите краткое или полное название страны: Пример: Америка."
# not_found_country = "🔴 Ma'lumot topilmadi, Iltimos qaytadan urinib ko'ring"
not_found_country_ru = "🔴Информация не найдена, попробуйте еще раз"
# select_one = "Quidagi mamlakatdan birini tanlang:"
select_one_ru = "Выберите одну из следующих стран:"

@dp.message_handler(text="🇷🇺Русский язык")
async def uz_lang(message: types.Message, state: FSMContext):
    await state.update_data(langauge_uz=False, language_ru=True) 
    await message.answer("Подать заявку на 2024-2025 учебный год", reply_markup=register_ru)


@dp.message_handler(text="🔄Трансферное обучение")
async def transfer_edu(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ic('rus tanlandi')

    all_data_state = await state.get_data() 
    token = all_data_state.get('token', None)
    ic('token72', token)
    if token is None:
        button_phone = types.KeyboardButton(text='📲 Отправьте номер телефона', request_contact=True)
        keyboard.add(button_phone)
        await message.answer(example_phone_ru, parse_mode="HTML",reply_markup=keyboard)
        await state.update_data(register_user=False, transfer_user=True)
        await PersonalDataRU.phone.set()
    elif token is not None:
        check_token = await send_req.application_forms_me(token)
        status_code = check_token.get('status_code')
        if status_code  == 200:
            await message.answer("🏠Главная страница", reply_markup=menu_ru)
        elif status_code != 200:
            refreshToken = all_data_state.get('refresh_token')
            if refreshToken is not None:
                new_token = await send_req.return_token_use_refresh(refreshToken)
                ic(new_token)


@dp.message_handler(Text(equals="🧾 Абитуриент"))
async def my_application(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ic('ru tanlandi')

    all_data_state = await state.get_data() 
    token = all_data_state.get('token', None)
    ic('token72', token)
    if token is None:
        button_phone = types.KeyboardButton(text='📲 Отправьте номер телефона', request_contact=True)
        keyboard.add(button_phone)
        await message.answer(example_phone_ru, parse_mode="HTML",reply_markup=keyboard)
        await state.update_data(register_user=True, transfer_user=False)
        await PersonalDataRU.phone.set()
    elif token is not None:
        check_token = await send_req.application_forms_me(token)
        status_code = check_token.get('status_code')
        if status_code  == 200:
            await message.answer("🏠Главная страница", reply_markup=menu_ru)
        elif status_code != 200:
            refreshToken = all_data_state.get('refresh_token')
            if refreshToken is not None:
                new_token = await send_req.return_token_use_refresh(refreshToken)
                ic(new_token)

@dp.message_handler(state=PersonalDataRU.phone, content_types=types.ContentTypes.CONTACT | types.ContentTypes.TEXT)
async def phone_contact_received(message: types.Message, state: FSMContext):
    # await message.answer(message.json())
    # ic(message)
    # ic(message.text)
    try:
        contact = message.contact
        phone_num = contact.phone_number
        ic('auto:', phone_num)
    except AttributeError:
        phone_num = None
        contact = None
    ic('next')
    try:
        custom_writened_phone = message.text
        ic(custom_writened_phone)
    except AttributeError:
        custom_writened_phone = None
    ic("custom_writened_phone", custom_writened_phone)
    # if contact is not None and phone_num is not None:
    ic(phone_num)
    ic('nomer keldi')
    if phone_num is not None:

        ic(phone_num, 100)
        ic(len(phone_num), 101)

        if str(phone_num)[0] != '+':
            phone_num = f"+{phone_num}"
            ic('plus qoshdi')
            if len(phone_num) == 13:
                custom_phone = phone_num
                ic(custom_phone, 102)
                check_user = await send_req.check_number(custom_phone)
                ic('check_user_new', check_user)
                ic(check_user)
                if check_user == 'true':
                    ic('check_user_for_true',check_user)
                    await state.update_data(phone=custom_phone)


                    user_login = await send_req.user_login(custom_phone)
                    
                    ic('user_login: ',user_login)
                    ic('user_login status: ',user_login.get('status_code'))
                    user_login_status = user_login.get('status_code')
                    ic('ru', user_login_status)

                    if user_login_status == 200:
                        ic('user_login status',user_login_status)
                        remove_keyboard = types.ReplyKeyboardRemove()
                        await message.answer(accepted_phone_ru, parse_mode='HTML', reply_markup=remove_keyboard)
                        await PersonalDataRU.secret_code.set()
                    else:
                        await message.answer("На сервере произошла ошибка")
                # ic(check_user)
                elif check_user == 'false':
                    ic('check_user_for_false', check_user)
                    await state.update_data(phone=custom_phone)
                    user_register = await send_req.user_register(custom_phone)
                    remove_keyboard = types.ReplyKeyboardRemove()
                    ic('user_register: ',user_register.status_code)
                    if user_register.status_code == 201:
                        await message.answer(accepted_phone_ru, reply_markup=remove_keyboard)
                        await PersonalDataRU.secret_code.set()

        elif len(phone_num) == 13:
            ic('plus bilan keldi')
            custom_phone = phone_num
            ic(custom_phone, 140)
            check_user = await send_req.check_number(custom_phone)
            ic('check_user_new', check_user)
            ic(check_user)
            if check_user == 'true':
                ic('check_user_for_true',check_user)
                await state.update_data(phone=custom_phone)


                user_login = await send_req.user_login(custom_phone)
                
                ic('user_login: ',user_login)
                ic('user_login status: ',user_login.get('status_code'))
                user_login_status = user_login.get('status_code')

                if user_login_status == 200:
                    ic('user_login status',user_login_status)
                    remove_keyboard = types.ReplyKeyboardRemove()
                    await message.answer(accepted_phone_ru, parse_mode='HTML', reply_markup=remove_keyboard)
                    await PersonalDataRU.secret_code.set()
                else:
                    await message.answer("severda xatolik yuz berdi")
            # ic(check_user)
            elif check_user == 'false':
                ic('check_user_for_false', check_user)
                await state.update_data(phone=custom_phone)
                user_register = await send_req.user_register(custom_phone)
                remove_keyboard = types.ReplyKeyboardRemove()
                ic('user_register: ',user_register.status_code)
                if user_register.status_code == 201:
                    await message.answer(accepted_phone_ru, reply_markup=remove_keyboard)
                    await PersonalDataRU.secret_code.set()

    elif custom_writened_phone is not None:
        custom_writened_phone = custom_writened_phone.strip()
        ic('custom_writened_phone: ',custom_writened_phone)
        status_while = True
        while status_while:
            ic('while ishladi ruschada')
            phone_num = custom_writened_phone.strip()
            if len(phone_num) != 12 or not phone_num.isdigit():
                await message.answer(error_message_phone_ru)
                response_msg = await dp.bot.send_message(message.chat.id, "Пожалуйста, введите номер телефона в правильном формате.")
                response = await dp.bot.wait_for("message")
                custom_writened_phone = message.text.strip() if response.text else None
                if custom_writened_phone:
                    phone_num = custom_writened_phone
                else:
                    break

            elif len(phone_num) == 12:
                ic('phone_num: 12talik',phone_num)
                status_while = False
                custom_phone = f'+{phone_num}'
                check_user = await send_req.check_number(custom_phone)
                ic('check_user', check_user)
                if str(check_user) == 'true':
                    await state.update_data(phone=custom_phone)
                    user_login = await send_req.user_login(custom_phone)
                    ic('user_login', user_login)
                    if user_login.get('status_code') == 200:
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        reset_pass_button = types.KeyboardButton(text='Отправить код повторно')
                        keyboard.add(reset_pass_button)
                        await message.answer(accepted_phone_simple_ru, reply_markup=ReplyKeyboardRemove())
                        await message.answer("Введите код, отправленный на ваш номер телефона", reply_markup=reset_pass_button)
                        await PersonalDataRU.secret_code.set()
                    else:
                        # await message.answer("935920479","severda xatolik 107")
                        await message.answer("Вы должны зарегистрироваться")

                elif str(check_user) == 'false':
                    await state.update_data(phone=custom_phone)
                    user_register = await send_req.user_register(custom_phone)
                    ic('user_register', user_register)
                    if user_register.get('status') == 200:
                        await message.answer(accepted_phone_ru, reply_markup=ReplyKeyboardRemove())
                        # await message.answer("Telefon raqamingizga yuborilgan kodni yuboring")
                        await PersonalDataRU.secret_code.set()
                else:
                    await message.answer("на сервере произошла ошибка")


@dp.message_handler(state=PersonalDataRU.secret_code)
async def secret_code(message: types.Message, state: FSMContext):
    secret_code = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if len(secret_code) == 6 and secret_code.isdigit():
        data = await state.get_data()
        phone_number = f"{data.get('phone')}"
        # ic("phone->", phone_number)
        response_ = await send_req.user_verify(int(secret_code), phone_number)
        res_status_code = response_.get('status_code')
        ic('response1111', response_)
        if response_.get('status_code') == 200:
            ic('kirdik333')
            # data_res = response_

            await state.update_data(token=response_.get('token'), refreshToken=response_.get('refreshToken'))
            data = await state.get_data()
            new_token_ = data.get('token')
            in_data = response_['data']
            # data_me_ = send_req.application_forms_me(new_token_)
            # data_me = data_me_.json()
            haveApplicationForm = in_data.get('haveApplicationForm')
            haveApplied = in_data.get('haveApplied')
            haveEducation = in_data.get('haveEducation')
            havePreviousEducation = in_data.get('havePreviousEducation')
            # ic(in_data)
            ic(haveApplicationForm)
            ic(haveApplied)
            ic(haveEducation)
            ic(havePreviousEducation)
            # ic(response_)
            ic(response_.get('status_code'))

            get_token = in_data.get('token')
            
            ic(get_token)
            try:
                await state.update_data(token=get_token)
                get_djtoken = await send_req.djtoken(username=USERNAME, password=PASSWORD)
                access = get_djtoken.get('access')
                ic(access)
                await state.update_data(access=access)
                user_chat_id = message.from_user.id
                ic(user_chat_id)
                date = message.date.strftime("%Y-%m-%d %H:%M:%S")
                ic(date)
                username = message.from_user.username or message.from_user.full_name
                ic(username)
                save_chat_id = send_req.create_user_profile(token=access, chat_id=user_chat_id, 
                                                                    first_name=message.from_user.first_name,                                                    last_name=message.from_user.last_name, 
                                                                    pin=1,date=date, username=username,
                                                                    university_name=int(UNIVERSITY_ID))
                ic(save_chat_id)

                get_this_user = send_req.get_user_profile(chat_id=user_chat_id, university_id=int(UNIVERSITY_ID))
                ic(get_this_user)
            except Exception as err:
                ic(err)
            if haveApplicationForm is False and (haveEducation is False and  havePreviousEducation is False) and haveApplied is False:
                await message.answer(example_document_ru, reply_markup=ReplyKeyboardRemove())
                await state.update_data(haveApplicationForm=True,haveEducation=False,havePreviousEducation=False,haveApplied=False)
                await PersonalDataRU.document.set()

            elif haveApplicationForm is True and (haveEducation is False and havePreviousEducation is False) and haveApplied is False:
                await message.answer("<i>- ✅Вы зарегистрированы.\n🔴Вам необходимо заполнить информацию о своем образовании</i>",reply_markup=enter_button)
                await state.update_data(haveApplicationForm=True,haveEducation=False,havePreviousEducation=False,haveApplied=False)
                ic('002')
                await PersonalDataRU.education_id.set()

            elif haveApplicationForm is True and (haveEducation is True and havePreviousEducation is False) and haveApplied is False:
                await message.answer("<i>- ✅ Вы зарегистрированы.\n- ✅ Также заполнена информация о вашем образовании.\n\nВы можете подать заявление в университет</i>", reply_markup=enter_button)
                await state.update_data(haveApplicationForm=True,haveEducation=True,havePreviousEducation=False,haveApplied=False)
                ic('keldi 003')
                await PersonalDataRU.degree_id.set()

            elif haveApplicationForm is True and (haveEducation is False and havePreviousEducation is True) and haveApplied is False:
                await message.answer("<i>- ✅ Вы зарегистрированы.\n- ✅ Также заполнена информация о вашем образовании.\n\nВы можете подать заявление в университет</i>", reply_markup=enter_button)
                await state.update_data(haveApplicationForm=True,haveEducation=False,havePreviousEducation=True,haveApplied=False)
                ic('keldi 003')
                await EducationDataRU.degree_id.set()

            elif haveApplicationForm is True and (haveEducation is True or havePreviousEducation is True) and haveApplied is True:
                await message.answer("<i>-✅​​Вы зарегистрированы\n-​​✅Также заполнена информация о вашем образовании,\n-✅​​Вы также подали заявление в университет.</i>", reply_markup=menu_ru)
                ic('keldi 004')
                await state.update_data(haveApplicationForm=True,haveEducation=False,havePreviousEducation=True,haveApplied=False)
                ic('keldi 005')
                await EducationDataRU.menu.set()



        
        elif res_status_code == 404 or res_status_code == 400 or res_status_code == 410:
            ic('\nres666',res_status_code, '\n')
            await message.answer(error_secret_code_ru)
            response_msg = await dp.bot.send_message(message.chat.id, retype_secret_code_ru)
            response = await dp.bot.wait_for("message")
    else:
        await message.answer(error_secret_code_ru)

    # remove_keyboard_ = types.ReplyKeyboardRemove()
    await state.update_data(secret_code=secret_code)



@dp.message_handler(state=PersonalDataRU.document)
async def document(message: types.Message, state: FSMContext):
    document = message.text.strip().upper()
    document_serial = document[:2]
    document_number = document[2:]

    while True:
        # Check if the serial and number parts are valid
        if len(document_serial) == 2 and document_serial.isalpha() and len(document_number) == 7 and document_number.isdigit():
            formatted_document = f'{document_serial}{document_number}'
            await state.update_data(document=formatted_document)
            break  # Exit loop if the document is valid
        
        # Handle invalid input
        await message.answer(error_document_ru)
        
        # Wait for a new user message as a response
        new_document = await message.answer("Пожалуйста, введите действительный документ:")
        document = (await dp.bot.wait_for("message")).text.strip().upper()
        document_serial = document[:2]
        document_number = document[2:]

    # After validation loop
    await message.answer(accepted_document_ru)
    await message.answer(example_birthday_ru)
    await PersonalDataRU.birth_date.set()


@dp.message_handler(state=PersonalDataRU.birth_date)
async def birth_date(message: types.Message, state: FSMContext):
    ic('birth date')
    birth_date = message.text.strip()
    # Check if the birth date format is valid
    birth_date_parts = birth_date.split('-') if birth_date else None
    # print('birth_date', birth_date_parts)
    if not birth_date_parts or len(birth_date_parts) != 3:
        await message.answer(error_message_birthday_ru)
        return

    check_year, check_month, check_day = birth_date_parts
    if not (check_day.isdigit() and check_month.isdigit() and check_year.isdigit()):
        await message.answer(error_message_birthday_ru)
        return

    year, month, day = map(int, birth_date_parts)
    # print(day, month, year)
    if not (1 <= day <= 31 and 1 <= month <= 12 and 2024 > year > 1990):
        await message.answer(error_date_ru)
        return
    

    data_state = await state.get_data()
    token = data_state.get('token')
    document = data_state.get('document')
    ic('birth_date', birth_date)
    ic("document", document)
    
    check_is_not_duplicate = await send_req.application_form_info(birth_date, document, token)
    ic(check_is_not_duplicate)

    if check_is_not_duplicate.get('status_code') in [500,404,400]:
        await message.answer(server_error_ru, reply_markup=enter_button_ru)
        await ManualPersonalInfo.personal_info.set()
    elif check_is_not_duplicate.get('status_code') == 409:
        error_mes = check_is_not_duplicate.get('data')
        
        await message.answer(f"🔴 {error_mes.get('message')}")
    # data_res = check_is_not_duplicate['data']
    # ic(check_is_not_duplicate)
    # if check_is_not_duplicate.get('status_code') == 409 or check_is_not_duplicate.get('status_code') == 401 or check_is_not_duplicate.get('status_code') == 400:
    #     # error_mes = data_res.get('message')
    #     await message.answer(f"🔴 {error_mes}")
    #     await state.finish()
    elif check_is_not_duplicate.get('status_code') == 200:
        await state.update_data(birth_date=birth_date)
        await message.answer(accepted_birthday_saved_data_ru)
        formatted_birth_date = f'{year}-{month}-{day}'
        await state.update_data(formatted_birth_date=formatted_birth_date)
        await message.answer(example_extra_phone_ru, reply_markup=ReplyKeyboardRemove())
        await PersonalDataRU.info.set()

   


@dp.message_handler(state=PersonalDataRU.info)
async def info(message: types.Message, state: FSMContext):
    extra_phone = message.text.strip()
    # ic('extra_phone', extra_phone)
    data = await state.get_data()
    ic('state ga saqlanganlar-->', data)
    formatted_birth_date = data.get('formatted_birth_date')
    document = data.get('document')
    new_token = data.get('new_token')
    token = data.get('token')
    ic('new_token', new_token)
    ic('token', token)
    # first_name = data.get('first_name')
    # last_name = data.get('last_name')
    phone = data.get('phone')
    ic(formatted_birth_date)
    date_obj = datetime.strptime(formatted_birth_date, "%Y-%m-%d")
    formatted_date_str = date_obj.strftime("%Y-%m-%d")

    ic('-->',formatted_date_str,document)
    response = await send_req.application_form_info(formatted_date_str,document,token)
    data = response['data']
    ic(response)
    # if response.get('status_code') == 409:
    #     await message.answer(response.get('message'))
    #     await state.finish()
    # else:
    data_res = data.get('passport', {})
    first_name = data_res.get('first_name', '')
    last_name = data_res.get('last_name', '')
    application_id = data_res.get('applicant_id', '')  # Note the key is 'applicant_id' based on your response
    third_name = data_res.get('third_name', '')
    document = data_res.get('document') if isinstance(data_res.get('document'), dict) else {}


    birth_country = data_res.get('birth_country', '')
    birth_country_id = data_res.get('birth_country_id', 0)
    birth_date = data_res.get('birth_date', '')
    birth_place = data_res.get('birth_place', '')
    citizenship = data_res.get('citizenship', '')
    gender = data_res.get('gender', '')
    photo = data_res.get('photo', '')
    pin = data_res.get('pin', [None])[0]
    
    docgiveplace = document.get('docgiveplace', '')
    docgiveplaceid = document.get('docgiveplaceid', 0)
    datebegin = document.get('datebegin', '')
    dateend = document.get('dateend', '')
    passort_serial = document.get('document')
    src = 'manually'
    user_datas = {
        "application_id": application_id,
        "birth_country": birth_country,
        "birth_country_id": birth_country_id,
        "birth_date": birth_date,
        "birth_place": birth_place,
        "citizenship": citizenship,
        "gender": gender,
        "photo": photo,
        "pin": pin,
        "document": document,
        "docgiveplace": docgiveplace,
        "docgiveplaceid": docgiveplaceid,
        "datebegin": datebegin,
        "dateend": dateend,
        "first_name": first_name,
        "last_name": last_name,
        "third_name": third_name,
        "src": src
    }
    ic(user_datas)
    await state.update_data(**user_datas)

    print('shu doc info', passort_serial)

    "def application_form(token, src, district_id, education_id, file_vs_format, institution_name, region_id):"

    response_application_form = send_req.application_form(token,
                                                        birth_date,
                                                        birth_place,
                                                        citizenship,
                                                        extra_phone,
                                                        first_name,
                                                        gender,
                                                        last_name,
                                                        phone,
                                                        photo,
                                                        pin,
                                                        passort_serial,
                                                        src,
                                                        third_name
                                                        )
    # ic(response_application_form.json())
    ic('keldi2022')
    data_me = await collect_data.collect_me_data(token, field_name=None)
    # ic(data_me)
    if response_application_form.status_code == 201:
        ic('keldi app formdan', response_application_form.status_code)
        application_data_res = response_application_form.json()
        application_id = application_data_res.get('applicant_id', '')
        application_src = application_data_res.get('application_src', '')
        user_education_src = application_data_res.get('user_education_src', '')
        which_level_need = application_data_res.get('which_level_need', '')
        country_id = application_data_res.get('country_id', '')
        country_name_uz = application_data_res.get('country_name_uz', '')
        country_name_ru = application_data_res.get('country_name_ru', '')
        country_name_en = application_data_res.get('country_name_ru', '')
        region_id = application_data_res.get('region_id', '')
        region_name_uz = application_data_res.get('region_name_uz', '')
        region_name_ru = application_data_res.get('region_name_ru', '')
        region_name_en = application_data_res.get('region_name_en', '')
        district_id = application_data_res.get('district_id', '')
        district_name_uz = application_data_res.get('district_name_uz', '')
        district_name_ru = application_data_res.get('district_name_ru', '')
        district_name_en = application_data_res.get('district_name_en', '')
        address = application_data_res.get('address','')
        father_name = application_data_res.get('father_name', '')
        father_phone = application_data_res.get('father_phone', '')
        mother_name = application_data_res.get('mother_name', '')
        pinfl_birth_country = application_data_res.get('pinfl_birth_country', '')
        pinfl_birth_country_id = application_data_res.get('pinfl_birth_country_id', '')
        created_at = application_data_res.get('created_at', '')
        pinfl_user_education = application_data_res.get('pinfl_user_education', '')
        user_education = application_data_res.get('user_education', '')
        certifications = application_data_res.get('certifications', [])
        data_obj_applications = {
            'application_src': application_src,
            'which_level_need': which_level_need,
            'user_education_src': user_education_src,
            'country_id': country_id,
            'country_name_uz': country_name_uz,
            'country_name_ru': country_name_ru,
            'country_name_en': country_name_en,
            'region_id': region_id,
            'region_name_uz': region_name_uz,
            'region_name_ru': region_name_ru,
            'region_name_en': region_name_en,
            'district_id': district_id,
            'district_name_uz': district_name_uz,
            'district_name_ru': district_name_ru,
            'district_name_en': district_name_en,
            'address': address,
            'father_name': father_name,
            'father_phone': father_phone,
            'mother_name': mother_name,
            'pinfl_birth_country': pinfl_birth_country,
            'pinfl_birth_country_id': pinfl_birth_country_id,
            'created_at': created_at,
            'pinfl_user_education': pinfl_user_education,
            'user_education': user_education,
            'certifications': certifications,
        }
        await state.update_data(**data_obj_applications)
        # await message.answer("Ta'lim malumotlarini kiriting")

        await message.answer("Нажмите «Продолжить», чтобы заполнить информацию об обучении.", reply_markup=enter_button_ru)
        ic('davom etish bosildi', 540)
        get_current_user = send_req.get_user_profile(chat_id=message.chat.id, university_id=UNIVERSITY_ID)
        chat_id_user = get_current_user['chat_id_user']
        id_user = get_current_user['id']
        await state.update_data(chat_id_user=chat_id_user, id_user=id_user)
        data = await state.get_data()
        phone = data['phone']
        ic('django')
        ic(id_user, phone, chat_id_user,first_name, last_name)
        try:
            update_user_profile_response = send_req.update_user_profile(
                university_id=UNIVERSITY_ID, 
                chat_id=chat_id_user, 
                phone=phone, 
                first_name=first_name, 
                last_name=last_name, 
                pin=pin,
                username=message.chat.username,
                date=message.date.strftime("%Y-%m-%d %H:%M:%S")
                )
            ic(update_user_profile_response)
        except Exception as e:
            ic(490,'my_dj_error', e)
        ic('education ga keldik', 598)

    data = await state.get_data()
    token = data.get('token')
    register_user = data.get('register_user')
    transfer_user = data.get('transfer_user')
    ic('register_user', register_user, 'transfer_user', transfer_user)

    if register_user:
        educations_response = send_req.educations(token)
        educations = educations_response.json()
        
        buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"edu_{item['id']}")]
                    for item in educations]
        educationMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("<b>Чтобы подать заявку в университет, вам необходимо ввести данные об образовании.</b>", parse_mode='HTML',
                            reply_markup=ReplyKeyboardRemove())
        await message.answer("<b>Выберите тип учебного заведения, которое вы окончили или учитесь:</b>", reply_markup=educationMenu, parse_mode='HTML')
            
        await EducationDataRU.education_id.set()
    await EducationDataRU.education_id.set()
    


@dp.message_handler(state=EducationDataRU.education_id)
async def education_id_handler(message: types.Message, state: FSMContext, page: int = 0):
    ic('education ga keldi')
    data = await state.get_data()
    token = data.get('token')
    register_user = data.get('register_user')
    transfer_user = data.get('transfer_user')
    ic('register_user', register_user, 'transfer_user', transfer_user)

    if register_user:
        educations_response = send_req.educations(token)
        educations = educations_response.json()
        
        buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"edu_{item['id']}")]
                   for item in educations]
        educationMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("<b>Чтобы подать заявку в университет, вам необходимо ввести данные об образовании.</b>", parse_mode='HTML')
        await message.answer("<b>Выберите тип учебного заведения, которое вы окончили или учитесь:</b>", reply_markup=educationMenu, parse_mode='HTML')
    elif transfer_user:
        # Ask user to input the search query for countries
        await EducationDataRU.country_search.set()  # Assuming country_search is a state for inputting country search
        await message.answer(search_university_ru, reply_markup=ReplyKeyboardRemove())

# Handle the country search input
@dp.message_handler(state=EducationDataRU.country_search)
async def process_country_search(message: types.Message, state: FSMContext):
    user_query = message.text.lower()
    token = (await state.get_data()).get('token')
    all_countries = await send_req.countries(token)  # Ensure this is an async call to your backend/API

    matching_countries = [country for country in all_countries if user_query in country['name_ru'].lower()]
    
    if not matching_countries:
        await message.answer(not_found_country_ru)
        return

    buttons = [
        [InlineKeyboardButton(text=country['name_ru'], callback_data=f"country_{country['id']}")]
        for country in matching_countries
    ]
    country_menu = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(select_one_ru, reply_markup=country_menu)
    await EducationDataRU.country_search.set()
    # await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('country_'), state=EducationDataRU.country_search)
async def handle_country_selection(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()  
    selected_country_id = callback_query.data.split('_')[1]
    ic('selected_country_id',selected_country_id)
    await state.update_data(country_id=selected_country_id)
    await callback_query.message.answer(saved_message_ru)
    await callback_query.message.answer("Введите название учебного заведения:... ", reply_markup=ReplyKeyboardRemove())
    await EducationDataRU.transfer_education_name.set()
    
@dp.message_handler(state=EducationDataRU.transfer_education_name)
async def transfer_education_name_handler(message: types.Message, state: FSMContext):
    transfer_edu_name = message.text.strip()
    ic(transfer_edu_name)
    await state.update_data(transfer_education_name=transfer_edu_name)
    await message.answer("Введите название направления обучения:... ", reply_markup=ReplyKeyboardRemove())
    await EducationDataRU.transfer_direction_name.set()


@dp.message_handler(state=EducationDataRU.transfer_direction_name)
async def transfer_direction_name_handler(message: types.Message, state: FSMContext):
    transfer_direction_name = message.text.strip()
    ic(transfer_direction_name)
    # await message.answer("Ayni vaqtdagi kursingizni tanlang: ")
    inline_buttons = [
        [
            InlineKeyboardButton(text='учусь на 1 курсе', callback_data=1)
        ],
        [
            InlineKeyboardButton(text='учусь на 2 курсе', callback_data=2)
        ]
    ]
    inline_kb = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    await message.answer("Выберите текущий курс: ", reply_markup=inline_kb)
    await state.update_data(transfer_direction_name=transfer_direction_name)

@dp.callback_query_handler(lambda c: c.data.isdigit(), state=EducationDataRU.transfer_direction_name)  # Ensures that only digit callback_data is processed here
async def handle_callback_query_dir(callback_query: types.CallbackQuery, state: FSMContext):
    selected_course = callback_query.data
    ic(selected_course)
    await callback_query.answer()
    await state.update_data(selected_course=selected_course)
    await callback_query.message.answer(example_transkript_message_ru, reply_markup=ReplyKeyboardRemove())
    await EducationDataRU.file_diploma_transkript.set()
    # await callback_query.message.answer()

@dp.message_handler(content_types=['document'], state=EducationDataRU.file_diploma_transkript)
async def upload_file(message: types.Message, state: FSMContext):
    ic(message.document.file_name)
    from aiogram import Bot, Dispatcher
    from data.config import BOT_TOKEN 
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot) 

    data = await state.get_data()
    ic(data)
    token_id = data['token']
    ic(token_id)
    
    token_ = data.get('token') if data.get('token') else None

    document = message.document
    file_path = await bot.get_file(document.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path.file_path}"
    ic(file_url)
    # await message.answer(file_url)
    download_dir = 'transcript_files'
    await aiofiles.os.makedirs(download_dir, exist_ok=True)

    local_file_path = os.path.join(download_dir, document.file_name)
    # print(local_file_path)
    await send_req.download_file(file_url, local_file_path)
    await message.answer(wait_file_is_loading_ru, parse_mode='HTML')
    # ic(local_file_path)

    res_file = upload.upload_new_file_transcript(token=token_, filename=local_file_path)
    # if file_size != 'File not found':
    try:
        file_size = os.path.getsize(local_file_path)
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024
        ic(f'size: {file_size_mb:.2f}')
    except: 
        return 'Файл не найден'
    await state.update_data(file_size=file_size)
    await message.answer("Файл загружен.")
    
    # ic(all_state)
    # print(res_file.status_code)
    # print(res_file)
    try:
        data1 = res_file.json()
        path = data1['path']
        ic(path)
        data = await state.get_data()
        file_diploma_transkript = path
        country_id = data.get('country_id')
        selected_course = data.get('selected_course')
        transfer_direction_name = data.get('transfer_direction_name')
        transfer_education_name = data.get('transfer_education_name')
        res_data = await send_req.application_forms_transfer(
            token_,
            int(country_id),
            transfer_direction_name,
            transfer_education_name,
            file_diploma_transkript,
            int(selected_course)
        )
        ic(res_data)
        await message.answer(saved_message_ru, reply_markup=enter_button_ru)
        await state.update_data(file_diploma_transkript=path)
        
    except Exception as e:
        ic(e)
        await message.answer(e)
        return e
    
    
    src_ = 'src' 
    src_res = await collect_data.collect_me_data(token=token_, field_name=src_)
    if src_res is not None or src_res is not False:
        await state.update_data(src=src_res)
    await EducationDataRU.degree_id.set()



@dp.callback_query_handler(lambda c: c.data.startswith('edu_'), state=EducationDataRU.education_id)
async def education_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN 
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    # from loader import dp
    education_id = callback_query.data.split('edu_')[1]
    await state.update_data(education_id=education_id)
    await callback_query.answer()
    await EducationDataRU.region_id.set() 
    await bot.send_message(callback_query.from_user.id, saved_message_ru, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    token = data['token']  # Corrected data access
    region_response = send_req.regions(token)  # Ensure it's awaited
    regions = region_response.json()  # Async call should be awaited
    
    buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"reg_{item['id']}")] for item in regions]
    regionMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(callback_query.from_user.id,select_region_ru, reply_markup=regionMenu)
    # await bot.send_message(callback_query.from_user.id, saved_message, reply_markup=enter_button, parse_mode="HTML")


# @dp.message_handler(state=EducationDataRU.region_id)
# async def select_region_id_handler(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     token = data['token']  # Corrected data access
#     region_response = send_req.regions(token)  # Ensure it's awaited
#     regions = region_response.json()  # Async call should be awaited
    
#     buttons = [[InlineKeyboardButton(text=item['name_uz'], callback_data=f"reg_{item['id']}")] for item in regions]
#     regionMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

#     await message.answer(select_region, reply_markup=regionMenu)



    

    
    # await message.answer("Ma'lumot saqlandi", reply_markup=ReplyKeyboardRemove)

@dp.callback_query_handler(lambda c: c.data.startswith('reg_'), state=EducationDataRU.region_id)
async def region_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    region_id = callback_query.data.split('reg_')[1]
    await state.update_data(region_id=region_id)
    await callback_query.answer()
    await EducationDataRU.district_id.set()  # Proceed to the next state
    
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    token = data['token']  # Use direct indexing for required data
    region_id = data['region_id']
    district_id_response = send_req.districts(token, int(region_id))  # Ensure it's awaited
    districts = district_id_response.json()  # Async call should be awaited
    # pprint(districts)
    buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"dist_{item['id']}")] for item in districts]
    districtsMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.answer("Выберите район:", reply_markup=districtsMenu)


# @dp.message_handler(state=EducationDataRU.district_id)
# async def education_id_handler(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     token = data['token']  # Use direct indexing for required data
#     region_id = data['region_id']
#     district_id_response = send_req.districts(token, int(region_id))  # Ensure it's awaited
#     districts = district_id_response.json()  # Async call should be awaited
#     # pprint(districts)
#     buttons = [[InlineKeyboardButton(text=item['name_uz'], callback_data=f"dist_{item['id']}")] for item in districts]
#     districtsMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    
#     await message.answer("Tumanni tanlang:", reply_markup=districtsMenu)

@dp.callback_query_handler(lambda c: c.data.startswith('dist_'), state=EducationDataRU.district_id)
async def district_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    district_id = callback_query.data.split('dist_')[1]
    await state.update_data(district_id=district_id)
    await callback_query.answer()
    await EducationDataRU.institution_name.set()  # Prepare for the next step
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN 
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot) 
    await bot.send_message(callback_query.from_user.id, type_your_edu_name_ru)

@dp.message_handler(state=EducationDataRU.institution_name)
async def type_institution_name_handler(message: types.Message, state: FSMContext):
    institution_name = message.text.strip()

    if institution_name.lower() != 'Продолжить':
        await state.update_data(institution_name=institution_name)
        await message.answer('Данные получены успешно.', reply_markup=ReplyKeyboardRemove())
        # Proceed to conclude the process or transition to the next state here
        # Example to conclude:
        data = await state.get_data()
        institution_name = data.get('institution_name', 'Не указан')
        await message.answer(example_diploma_message_ru, parse_mode="Markdown")
        await EducationDataRU.file_diploma.set() 
    else:
        # If the user sends 'Davom etish', prompt them again for the institution name.
        await message.answer(error_type_edu_name_ru, reply_markup=enter_button_ru)

@dp.message_handler(content_types=['document'], state=EducationDataRU.file_diploma)
async def upload_file(message: types.Message, state: FSMContext):
    from aiogram import Bot, Dispatcher
    from data.config import BOT_TOKEN 
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot) 

    data = await state.get_data()
    token_ = data['token'] if data['token'] else None

    document = message.document
    file_path = await bot.get_file(document.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path.file_path}"
    # ic(file_url)
    # await message.answer(file_url)
    download_dir = 'diploma_files'
    await aiofiles.os.makedirs(download_dir, exist_ok=True)

    local_file_path = os.path.join(download_dir, document.file_name)
    # print(local_file_path)
    await send_req.download_file(file_url, local_file_path)
    await message.answer(wait_file_is_loading_ru, parse_mode='HTML')
    # ic(local_file_path)

    res_file = upload.upload_new_file(token=token_, filename=local_file_path)
    # if file_size != 'File not found':
    try:
        file_size = os.path.getsize(local_file_path)
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024
        # print(f'size: {file_size_mb:.2f}')
    except: 
        return 'Файл не найден'
    await state.update_data(file_size=file_size)
    await message.answer("Файл загружен.")
    
    # ic(all_state)
    # print(res_file.status_code)
    # print(res_file)
    try:
        data1 = res_file.json()
        ic(data1['path'])
        await state.update_data(file_diploma=data1['path'])
    except Exception as e:
        return e
    

    src_ = 'src' 
    src_res = await collect_data.collect_me_data(token=token_, field_name=src_)
    if src_res is not None or src_res is not False:
        await state.update_data(src=src_res)
    


    all_state = await state.get_data()
    ic(all_state)
    # print(data1['path'])
    district_id = int(all_state['district_id']) if all_state['district_id'] else 0
    education_id = int(all_state['education_id']) if all_state['education_id'] else 0
    file_ = all_state['file_diploma'] if all_state['file_diploma'] else None
    institution_name = all_state['institution_name'] if all_state['institution_name'] else None
    region_id = int(all_state['region_id']) if all_state['region_id'] else None
    src = all_state['src'] if all_state['src'] else 'manually'

    res_data_app_forms_for_edu = send_req.application_forms_for_edu(token_,
                                                    district_id,
                                                    education_id,
                                                    file_,
                                                    institution_name,
                                                    region_id,
                                                    src
                                                    )
    await state.update_data(me_data=res_data_app_forms_for_edu.json())
    await message.answer("<b>Есть ли у вас сертификат по иностранному языку?</b>", parse_mode='HTML', reply_markup=yes_no_ru)
    # ic(res_data_app_forms_for_edu.json())

    await EducationDataRU.has_sertificate.set()

@dp.message_handler(state=EducationDataRU.has_sertificate)
async def has_sertificate(message: types.Message, state: FSMContext):

    text = message.text
    if text == "Да, есть":
        cert_types = [
            {'id': 1, 'type': 'IELTS'},
            {'id': 2, 'type': 'TOEFL'},
            {'id': 3, 'type': 'CEFR'},
            {'id': 4, 'type': 'SAT'},
            {'id': 5, 'type': 'GMAT'},
            {'id': 6, 'type': 'GRE'},
            {'id': 7, 'type': 'Другой'}
        ] 
        buttons = [[InlineKeyboardButton(text=item['type'], 
                                        callback_data=f"type_{item['id']}") for item in cert_types]]
        certTypeMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(select_type_certificate_ru, reply_markup=certTypeMenu)
        await EducationDataRU.certificate_type.set()


    elif text == "Нет, не доступен":
        await message.answer("Если вы хотите заполнить образовательную информацию, нажмите кнопку «Продолжить».", reply_markup=enter_button_ru)

        await EducationDataRU.degree_id.set()
        
    

@dp.callback_query_handler(lambda c: c.data.startswith('type_'), state=EducationDataRU.certificate_type)
async def region_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    certificate_type = callback_query.data.split('type_')[1]
    cert_types = [
            {'id': 1, 'type': 'IELTS'},
            {'id': 2, 'type': 'TOEFL'},
            {'id': 3, 'type': 'CEFR'},
            {'id': 4, 'type': 'SAT'},
            {'id': 5, 'type': 'GMAT'},
            {'id': 6, 'type': 'GRE'},
            {'id': 7, 'type': 'Другой'}
        ] 
    cert_types = [item['type'] for item in cert_types if item['id'] == int(certificate_type)]
    ic(cert_types)
    if certificate_type and len(cert_types) > 0:
        certificate_type = str(cert_types[0]).lower()
        ic(certificate_type)
    await state.update_data(certificate_type=certificate_type)
    await callback_query.answer()
    await EducationDataRU.get_certificate.set()  # Proceed to the next state
    # await message.answer(c)
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML")
    await callback_query.message.answer(example_certification_message_ru, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

# await message.answer(example_certification_message) 
@dp.message_handler(content_types=['document'], state=EducationDataRU.get_certificate)
async def get_sertificate(message: types.Message, state: FSMContext):
    from aiogram import Bot, Dispatcher
    from data.config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    
    data = await state.get_data()
    token_ = data['token'] if data['token'] else None

    document = message.document
    file_path = await bot.get_file(document.file_id)
    ic(file_path)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path.file_path}"
    download_dir = 'sertificate_files'
    # await message.answer(file_url)
    await aiofiles.os.makedirs(download_dir, exist_ok=True)

    local_file_path = os.path.join(download_dir, document.file_name)
    ic(local_file_path)
    await send_req.download_file(file_url, local_file_path)
    await message.answer(wait_file_is_loading_ru, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    # ic(local_file_path)

    res_file = upload.upload_new_file_sertificate(token=token_, filename=local_file_path)
    ic(731, res_file)
    try:
        file_size = os.path.getsize(local_file_path)
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024
        ic(f'size: {file_size_mb:.2f}')
    except:
        return 'Файл не найден'
    await state.update_data(file_size_sertificate=file_size)
    # await message.answer("Fayl yuklandi.", reply_markup=ReplyKeyboardRemove())
    # await EducationDataRU.has_application.set()
    # ic(all_state)
    ic(res_file.status_code)
    ic(res_file)
    data_user = await state.get_data()
    certificate_type = data_user['certificate_type']
    ic(certificate_type)
    data1 = res_file.json()
    ic(747, data1)
    await state.update_data(file_sertificate=data1['path'])
    ic(token_)
    ic(data1['path'])
    try:
        res = send_req.upload_sertificate(token=token_, filename=data1['path'], f_type=certificate_type)
        ic(751, res)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
        return

    await message.answer("Файл загружен.")
    ic('boshlandi1')
    await EducationDataRU.degree_id.set()
    ic('yakunlandi')
    await message.answer("<b>Подача заявления в университет</b>", parse_mode="HTML")
    ic('started')
    my_degree = {1: 'Бакалавр',2: 'Магистратура',3: 'Докторантура'}
    data = await state.get_data()
    token = data['token']
    directions_response = await send_req.directions(token)
    directions = directions_response
    unique_degrees = []
    ic('ok')
    for obj in directions:
        degree_id = obj['degree_id']
        if not any(d['id'] == degree_id for d in unique_degrees):
            unique_degrees.append({
                'id': degree_id,
                'type_degree': my_degree[degree_id]})
    ic(unique_degrees)
    buttons = [[InlineKeyboardButton(text=item['type_degree'], 
                                     callback_data=f"degree_{item['id']}") for item in unique_degrees]]
    degreeMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    ic('keldi')
    await message.answer(select_degree_ru, parse_mode='HTML', reply_markup=degreeMenu)


@dp.message_handler(state=EducationDataRU.degree_id)
async def has_application_start(message: types.Message, state: FSMContext):
    await message.answer("<b>Подача заявления в университет</b>", parse_mode="HTML")
    ic('started')
    my_degree = {1: 'Бакалавр',2: 'Магистратура',3: 'Докторантура'}
    data = await state.get_data()
    token = data['token']
    directions_response = await send_req.directions(token)
    directions = directions_response
    unique_degrees = []
    ic('ok')
    for obj in directions:
        degree_id = obj['degree_id']
        if not any(d['id'] == degree_id for d in unique_degrees):
            unique_degrees.append({
                'id': degree_id,
                'type_degree': my_degree[degree_id]})
    ic(unique_degrees)
    buttons = [[InlineKeyboardButton(text=item['type_degree'], 
                                     callback_data=f"degree_{item['id']}") for item in unique_degrees]]
    degreeMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    ic('keldi')
    await message.answer(select_degree_ru, parse_mode='HTML', reply_markup=degreeMenu)
    



@dp.callback_query_handler(lambda c: c.data.startswith('degree_'), state=EducationDataRU.degree_id)
async def has_application(callback_query: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot
    from data.config import BOT_TOKEN 

    bot = Bot(token=BOT_TOKEN)
    degree_id = callback_query.data.split('degree_')[1]
    ic(degree_id)
    await state.update_data(degree_id=degree_id)
    await callback_query.answer()
    await EducationDataRU.direction_id.set()
 
    await bot.send_message(callback_query.from_user.id, saved_message_ru, reply_markup=ReplyKeyboardRemove(),
                           parse_mode="HTML")
    data = await state.get_data()
    token = data['token']  
    region_response =await send_req.directions(token) 
    regions = region_response
    selected_degree_id = data['degree_id']
    ic(selected_degree_id)
    buttons = [[InlineKeyboardButton(text=item['direction_name_ru'], 
                                     callback_data=f"direc_{item['direction_id']}")] 
                                     for item in regions
                                       if item['degree_id'] == int(selected_degree_id)]
    directionMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(callback_query.from_user.id, select_direction_ru, reply_markup=directionMenu)
    



# @dp.message_handler(state=EducationDataRU.direction_id)
# async def direction_id_select(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     token = data['token']  
#     region_response =await send_req.directions(token) 
#     regions = region_response
#     selected_degree_id = data['degree_id']
#     ic(selected_degree_id)
#     buttons = [[InlineKeyboardButton(text=item['direction_name_uz'], 
#                                      callback_data=f"direc_{item['direction_id']}")] 
#                                      for item in regions
#                                        if item['degree_id'] == int(selected_degree_id)]
#     directionMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

#     await message.answer(select_direction, reply_markup=directionMenu)
    

@dp.callback_query_handler(lambda c: c.data.startswith('direc_'), state=EducationDataRU.direction_id)
async def region_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    direction_id = callback_query.data.split('direc_')[1]
    await state.update_data(direction_id=direction_id)
    await callback_query.answer()
    await EducationDataRU.education_type.set()  # Proceed to the next state
    
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML")
    data = await state.get_data()
    token = data['token']
    selected_degree_id = int(data['degree_id'])
    selected_direction_id = int(data['direction_id'])
    ic(selected_degree_id)
    ic(selected_direction_id)
    edu_type_response =await send_req.directions(token)
    edu_types = edu_type_response
    def return_edu_type_name_uz(edu_type_id):
        for edu in edu_types:
            direction_id = edu['direction_id']
            degree_id = edu['degree_id']
            education_types = edu['education_types']
            if edu['direction_id'] == direction_id and edu['degree_id'] == degree_id:
                for k in education_types:
                    if k['education_type_id'] == edu_type_id:
                        return k['education_type_name_ru']
        return None

    uniq_edu_types = []
    for obj in edu_types:
        direction_id = obj['direction_id']
        degree_id = obj['degree_id']
        if selected_degree_id == degree_id and direction_id == selected_direction_id:
            
            tuition_fees = obj['tuition_fees']
            for k in tuition_fees:
                education_type_id = k['education_type_id']
                edu_type_name = return_edu_type_name_uz(education_type_id)
                if edu_type_name:
                    obj = {
                            'id': education_type_id,
                            'name': edu_type_name
                        }
                    ic(obj)
                    if obj not in uniq_edu_types:
                        uniq_edu_types.append(obj)
    
    buttons = [[InlineKeyboardButton(text=item['name'], callback_data=f"edu_type_{item['id']}")] for item in uniq_edu_types]
    eduTypesMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.answer(select_edu_type_ru, reply_markup=eduTypesMenu)



# @dp.message_handler(state=EducationDataRU.education_type)
# async def direction_id_select(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     token = data['token']
#     selected_degree_id = int(data['degree_id'])
#     selected_direction_id = int(data['direction_id'])
#     ic(selected_degree_id)
#     ic(selected_direction_id)
#     edu_type_response =await send_req.directions(token)
#     edu_types = edu_type_response
#     def return_edu_type_name_uz(edu_type_id):
#         for edu in edu_types:
#             direction_id = edu['direction_id']
#             degree_id = edu['degree_id']
#             education_types = edu['education_types']
#             if edu['direction_id'] == direction_id and edu['degree_id'] == degree_id:
#                 for k in education_types:
#                     if k['education_type_id'] == edu_type_id:
#                         return k['education_type_name_uz']
#         return None

#     uniq_edu_types = []
#     for obj in edu_types:
#         direction_id = obj['direction_id']
#         degree_id = obj['degree_id']
#         if selected_degree_id == degree_id and direction_id == selected_direction_id:
            
#             tuition_fees = obj['tuition_fees']
#             for k in tuition_fees:
#                 education_type_id = k['education_type_id']
#                 edu_type_name = return_edu_type_name_uz(education_type_id)
#                 if edu_type_name:
#                     obj = {
#                             'id': education_type_id,
#                             'name': edu_type_name
#                         }
#                     ic(obj)
#                     if obj not in uniq_edu_types:
#                         uniq_edu_types.append(obj)
    
#     buttons = [[InlineKeyboardButton(text=item['name'], callback_data=f"edu_type_{item['id']}")] for item in uniq_edu_types]
#     eduTypesMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
#     await message.answer(select_edu_type, reply_markup=eduTypesMenu)
  

@dp.callback_query_handler(lambda c: c.data.startswith('edu_type_'), state=EducationDataRU.education_type)
async def region_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    edu_type_id_ = callback_query.data.split('edu_type_')[1]
    ic(866, edu_type_id_)
    await state.update_data(education_type=edu_type_id_)
    await callback_query.answer()
    await EducationDataRU.education_lang_id.set() 
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML")
    data = await state.get_data()
    token = data['token']  
    education_type_id_selected = int(data['education_type'])
    direction_id_selected = int(data['direction_id'])
    degree_id_selected = int(data['degree_id'])
    edu_lang_response = await send_req.directions(token)  
    edu_languages = edu_lang_response
    edu_langs = []
    def return_language_name(language_id):
        for obj in edu_languages:
            education_languages = obj['education_languages']
            for lang in education_languages:
                education_language_id = int(lang['education_language_id'])
                if language_id == education_language_id:
                    return lang['education_language_name_ru']
        return None
    for obj in edu_languages:
        direction_id = int(obj['direction_id'])
        degree_id = int(obj['degree_id'])
        if direction_id == direction_id_selected and degree_id == degree_id_selected:
            tuition_fees = obj['tuition_fees']
            for t in tuition_fees:
                education_language_id = int(t['education_language_id'])
                education_type_id = int(t['education_type_id'])
                if education_type_id == education_type_id_selected:
                    get_lang_name = return_language_name(education_language_id)
                    if get_lang_name:
                        lang_obj = {
                            'name': get_lang_name,
                            'id': education_language_id,
                            'tuition_fee': t['tuition_fee']
                        }
                        if lang_obj not in edu_langs:
                            ic(lang_obj)
                            edu_langs.append(lang_obj)

    buttons = [[InlineKeyboardButton(text=item['name'], callback_data=f"_{item['id']}_{item['tuition_fee']}")] for item in edu_langs]
    languageMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.answer(select_edu_language_ru, reply_markup=languageMenu)




# @dp.message_handler(state=EducationDataRU.education_lang_id)
# async def lang_id_select(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     token = data['token']  
#     education_type_id_selected = int(data['education_type'])
#     direction_id_selected = int(data['direction_id'])
#     degree_id_selected = int(data['degree_id'])
#     edu_lang_response = await send_req.directions(token)  
#     edu_languages = edu_lang_response
#     edu_langs = []
#     def return_language_name(language_id):
#         for obj in edu_languages:
#             education_languages = obj['education_languages']
#             for lang in education_languages:
#                 education_language_id = int(lang['education_language_id'])
#                 if language_id == education_language_id:
#                     return lang['education_language_name_uz']
#         return None
#     for obj in edu_languages:
#         direction_id = int(obj['direction_id'])
#         degree_id = int(obj['degree_id'])
#         if direction_id == direction_id_selected and degree_id == degree_id_selected:
#             tuition_fees = obj['tuition_fees']
#             for t in tuition_fees:
#                 education_language_id = int(t['education_language_id'])
#                 education_type_id = int(t['education_type_id'])
#                 if education_type_id == education_type_id_selected:
#                     get_lang_name = return_language_name(education_language_id)
#                     if get_lang_name:
#                         lang_obj = {
#                             'name': get_lang_name,
#                             'id': education_language_id,
#                             'tuition_fee': t['tuition_fee']
#                         }
#                         if lang_obj not in edu_langs:
#                             ic(lang_obj)
#                             edu_langs.append(lang_obj)

#     buttons = [[InlineKeyboardButton(text=item['name'], callback_data=f"_{item['id']}_{item['tuition_fee']}")] for item in edu_langs]
#     regionMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
#     await message.answer(select_edu_language, reply_markup=regionMenu)

@dp.callback_query_handler(lambda c: c.data.startswith('_'), state=EducationDataRU.education_lang_id)
async def after_select_lang(callback_query: types.CallbackQuery, state: FSMContext):
    ic(callback_query.data)
    
    parts = callback_query.data[1:].split('_')

    if len(parts) < 2:
        await callback_query.message.answer("Неверный формат данных ")
        return

    education_lang_id, eduaction_tuition_fee = parts
    ic(education_lang_id, eduaction_tuition_fee)
    await state.update_data(education_lang_id=education_lang_id, tuition_fee=eduaction_tuition_fee)

    all_state_data = await state.get_data()
    # ic(all_state_data)
    await callback_query.answer()
    await EducationDataRU.menu.set()
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML")
    await callback_query.message.answer(
        f"✅ <b>Цена выбранного направления</b>\n"
        f"--------------------------------\n"
        f"💵 <i>Цена:</i> <b>{all_state_data['tuition_fee']}</b> сум\n",
        parse_mode='HTML'
    )
    new_state_data = await state.get_data()
    ic(all_state_data.get('degree_id'), new_state_data.get('direction_id'), all_state_data.get('education_type'), new_state_data.get('education_lang_id'))

    degree_id = int(new_state_data.get('degree_id'))
    direction_id = int(new_state_data.get('direction_id'))
    education_language_id = int(new_state_data.get('education_lang_id'))
    education_type_id = int(new_state_data.get('education_type'))
    token_ = new_state_data.get('token')

    applicant = await send_req.applicants(token_, degree_id, direction_id, education_language_id, education_type_id, work_experience_document=None)
    # ic(applicant)
    
    if applicant is not None:
        await callback_query.message.answer(application_submited_ru, reply_markup=menu_ru)
        await EducationDataRU.menu.set()
    else:
        await callback_query.message.answer("Произошла ошибка, администратор предупрежден, повторите попытку позже.")
        
 


