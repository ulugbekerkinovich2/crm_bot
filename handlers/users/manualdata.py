from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from utils import send_req
from loader import dp
from states.personalData import PersonalData, EducationData, ManualPersonalInfo
from aiogram.utils.exceptions import Throttled
from data.config import throttling_time, domain_name
from pprint import pprint
import datetime
from handlers.users import collect_data, upload
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove,ParseMode
import os
import aiofiles.os
from icecream import ic
import json
import re
from keyboards.default.registerKeyBoardButton import yes_no
from keyboards.default.registerKeyBoardButton import enter_button, menu
from handlers.users.register import error_message_birthday, error_date,error_document,accepted_document,error_pin, error_number,error_birthplace,wait_file_is_loading
from data.config import university_id as UNIVERSITY_ID
async def send_photo_from_message(message: types.Message, photo_url: str, caption: str):
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=caption,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )

# @dp.message_handler(Text(equals="ok"), state=None)
@dp.message_handler(state=ManualPersonalInfo.personal_info)
async def send_welcome(message: types.Message, state: FSMContext):
    photo_url = "https://api.mentalaba.uz/logo/20fb9b17-4807-410d-8933-b611a63f5efd.png"
    caption = "Rasmingizni yuboring 3x4 formatda. jpg, png formatda"
    await send_photo_from_message(message, photo_url, caption)
    await ManualPersonalInfo.image.set()

@dp.message_handler(state=ManualPersonalInfo.image, content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT])
async def get_image(message: types.Message, state: FSMContext):
    from aiogram import Bot, Dispatcher
    from data.config import BOT_TOKEN 
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    data = await state.get_data()
    token_ = data.get('token', None)
    ic(token_)
    ic(message)
    download_dir = 'profile_images'
    if message.photo:
        try:
            largest_photo = message.photo[-1]
            ic(largest_photo)
            file_id = largest_photo.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            ic(file_path)
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            # await message.answer(file_url)
            
            local_file_path = os.path.join(download_dir, file_path) 
            await bot.download_file(file_path, local_file_path)
            try:
                res_file = upload.upload_new_file(token=token_, filename=local_file_path)
                data1 = res_file.json()
                ic(data1)
                await state.update_data(image=data1['path'])
            except Exception as e:
                ic(e)
                await message.reply(f"Xatolik yuz berdi: {str(e)}")
            await message.reply("Rasm qabul qilindi")
            await message.answer("Familiyangizni kiriting\nNamuna: Abdullayev")
            await ManualPersonalInfo.lastname.set()
        except Exception as e:
            await message.reply("Iltimos, rasm yuboring. Rasmlar 3x4 formatda bo'lishi kerak.")

    elif not message.photo:
        try:
            document = message.document
            file_path = await bot.get_file(document.file_id)
            ic(file_path)
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path.file_path}"

            await aiofiles.os.makedirs(download_dir, exist_ok=True)
            local_file_path = os.path.join(download_dir, document.file_name)
            ic(local_file_path)
            await send_req.download_file(file_url, local_file_path)
            await message.answer(wait_file_is_loading, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
            try:
                res_file = upload.upload_new_file(token=token_, filename=local_file_path)
                data1 = res_file.json()
                ic(data1)
                await state.update_data(image=data1['path'])
            except Exception as e:
                ic(e)
                await message.reply(f"Faylni qayta ishlashda xatolik yuz berdi: {str(e)}")
        except Exception as e:
            ic(e)
            await message.reply("Iltimos, rasm yuboring. Rasmlar 3x4 formatda bo'lishi kerak.\nSiz yuborilgan fayl qabul qilinmadi")
        await message.reply("Rasm qabul qilindi")
        await message.answer("Familiyangizni kiriting\nNamuna: Abdullayev")
        await ManualPersonalInfo.lastname.set()

@dp.message_handler(state=ManualPersonalInfo.lastname)
async def get_lastname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text.strip()
        last_name = data['lastname']
        await state.update_data(lastname=last_name)
    await message.answer("Ismingizni kiriting Namuna: Alisher")
    await ManualPersonalInfo.firstname.set()

@dp.message_handler(state=ManualPersonalInfo.firstname)
async def get_firstname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text.strip()
        first_name = data['firstname']
        await state.update_data(firstname=first_name)
    await message.answer("Otangizni ismini kiriting\nNamuna: Najmiddin")
    await ManualPersonalInfo.thirdname.set()

@dp.message_handler(state=ManualPersonalInfo.thirdname)
async def get_thirdname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['thirdname'] = message.text.strip()
        third_name = data['thirdname']
        await state.update_data(thirdname=third_name)
    await message.answer("Passport seriyasini kiriting\nNamuna: AB1234567")
    await ManualPersonalInfo.document.set()

@dp.message_handler(state=ManualPersonalInfo.document)
async def get_document(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['document'] = message.text.strip()
        document = data['document'].upper()
        document_serial = document[:2]
        document_number = document[2:]

        while True:
            # Check if the serial and number parts are valid
            if len(document_serial) == 2 and document_serial.isalpha() and len(document_number) == 7 and document_number.isdigit():
                formatted_document = f'{document_serial}{document_number}'
                await state.update_data(document=formatted_document)
                break  # Exit loop if the document is valid
            
            # Handle invalid input
            await message.answer(error_document)
            
            # Wait for a new user message as a response
            new_document = await message.answer("Iltimos, passport seriyasini namunadagidek kiriting\nNamuna: AB1234567:")
            new_document = await dp.bot.wait_for("message", lambda msg: msg.chat.id == message.chat.id)
            document = new_document.text.strip().upper()
            document_serial = document[:2]
            document_number = document[2:]

        # After validation loop
        await message.answer(accepted_document)
    await message.answer("Tug'ilgan sanasini kiriting\nNamuna: yyyy-oo-kk, 2002-03-21")
    await ManualPersonalInfo.birthdate.set()

@dp.message_handler(state=ManualPersonalInfo.birthdate)
async def get_birthdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['birthdate'] = message.text.strip()
        birth_date = data['birthdate']
        birth_date_parts = birth_date.split('-') if birth_date else None
        # print('birth_date', birth_date_parts)
        if not birth_date_parts or len(birth_date_parts) != 3:
            await message.answer(error_message_birthday)
            return

        check_year, check_month, check_day = birth_date_parts
        if not (check_day.isdigit() and check_month.isdigit() and check_year.isdigit()):
            await message.answer(error_message_birthday)
            return

        year, month, day = map(int, birth_date_parts)
        # print(day, month, year)
        if not (1 <= day <= 31 and 1 <= month <= 12 and 2014 > year > 1800):
            await message.answer(error_date)
            return
        await state.update_data(birthdate=birth_date)
        await message.answer("JSHSHR ni kiriting\nNamuna: 12345678901234")
        await ManualPersonalInfo.pin.set()

@dp.message_handler(state=ManualPersonalInfo.pin)
async def get_pin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pin'] = message.text.strip()
        pinfl = data['pin']
        ic(pinfl)
        if len(pinfl) != 14 or not pinfl.isdigit():
            await message.answer(error_pin)
            return
    await state.update_data(pin=pinfl)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("Erkak"), KeyboardButton("Ayol"))
    await message.answer("Jinsni tanlang", reply_markup=keyboard)
    await ManualPersonalInfo.gender.set()

@dp.message_handler(lambda message: message.text not in ["Erkak", "Ayol"], state=ManualPersonalInfo.gender)
async def gender_invalid(message: types.Message):
    await message.reply("Iltimos, jinsingizni 'Erkak' yoki 'Ayol' dan birini tanlang.")

@dp.message_handler(lambda message: message.text in ["Erkak", "Ayol"], state=ManualPersonalInfo.gender)
async def get_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ic(data)
        data['gender'] = message.text
        gender = data['gender']
        if gender == "Erkak":
            await state.update_data(gender="male")
        else:
            await state.update_data(gender="female")
    await message.answer("Tug'ilgan joyingizi kiriting Namuna: Toshkent shahri", reply_markup=ReplyKeyboardRemove())
    await ManualPersonalInfo.birthplace.set()

@dp.message_handler(state=ManualPersonalInfo.birthplace)
async def get_birthplace(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ic(data)
        data['birthplace'] = message.text.strip()
        birth_place = data['birthplace']
        if not birth_place:
            await message.answer(error_birthplace)
            return
    await state.update_data(birthplace=birth_place)
    await message.answer("Qo'shimcha telefon raqamingizni kiriting Namuna: 901234567")
    await ManualPersonalInfo.extranumber.set()

@dp.message_handler(state=ManualPersonalInfo.extranumber)
async def get_extranumber(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['extranumber'] = message.text.strip()
        
        extra_num = data['extranumber']
        if not extra_num.isdigit() and len(extra_num) != 9:
            await message.answer(error_number)
            return
    extra_num = f"+998{data['extranumber']}"
    await state.update_data(extranumber=extra_num)
    await message.answer("Emailingizni kiriting\n Namuna: yigitaliyeva@gmail.com")
    await ManualPersonalInfo.email.set()

@dp.message_handler(state=ManualPersonalInfo.email)
async def get_email(message: types.Message, state: FSMContext):
    email = message.text.strip()
    ic(218, email)
    # Debug prints can be removed or handled via logging
    # Logging example: logger.debug(f"Received email: {email}")
    
    if not "@gmail.com" in email:
        await message.answer("Email yaroqli emas. Iltimos yaroqli email kiriting. Email kichik harflardan tashkil topgan bo'lishi kerak.")
    

    await state.update_data(email=email)
    data_obj = await state.get_data()
    token = data_obj.get('token')
    lastname = data_obj.get('lastname')
    firstname = data_obj.get('firstname')
    thirdname = data_obj.get('thirdname')
    document = data_obj.get('document')
    birthdate = data_obj.get('birthdate')
    pinfl = data_obj.get('pin')
    gender = data_obj.get('gender')

    if gender == "Erkak":
        gender = "male"
    else:
        gender = "female"

    birthplace = data_obj.get('birthplace')
    extranumber = data_obj.get('extranumber')
    email_ = data_obj.get('email')
    image = data_obj.get('image')
    phone = data_obj.get('phone')
    src_ = "manually"

    get_current_user = send_req.get_user_profile(chat_id=message.chat.id, university_id=UNIVERSITY_ID)
    chat_id_user = get_current_user['chat_id_user']
    id_user = get_current_user['id']

    await state.update_data(chat_id_user=chat_id_user, id_user=id_user)
    data = await state.get_data()
    phone = data['phone']
    ic('django')
    ic(id_user, email, chat_id_user,firstname, lastname)


    # Get the current date and time
    date_now = datetime.datetime.now()
    date_now_formatted = date_now.strftime('%Y-%m-%d %H:%M:%S')
    # try: 
    update_user_profile_response = send_req.update_user_profile(university_id=UNIVERSITY_ID, chat_id=chat_id_user, phone=phone, first_name=firstname, last_name=lastname, pin=pinfl,
                                                                username=message.from_user.username, date=date_now_formatted)
    ic(update_user_profile_response)
    # except Exception as e:
    #     ic(490,'my_dj_error', e)
    try:
        ic(gender, birthdate, birthplace, extranumber)
        res_app_forms = send_req.application_form_manual(token, birthdate,birthplace,email_,extranumber,firstname,
                                            gender,lastname,phone,image,pinfl,document,
                                        src_,thirdname)
        ic(res_app_forms)
    except Exception as e:
        return await message.answer(res_app_forms['data']['message'])
    # ic(res_app_forms.get('status_code'))
    if res_app_forms.get('status_code') == 201:
        ic(res_app_forms.get('status_code'))
        await message.answer("Ma'lumotlaringiz saqlandi", reply_markup=enter_button)
        res_me = await send_req.application_forms_me_new(token)
        ic(res_me)
        res_me.get('status_code')
        if res_me.get('status_code') == 200:
            user_education_src = res_me['data'].get('user_education_src', None)
            if user_education_src is None:
                await EducationData.education_id.set()
            elif user_education_src is not None:
                await EducationData.degree_id.set()
    else:
        await message.answer("Ma'lumotlaringiz saqlanmadi, qayta email kiriting.")
        # await message.answer(res_app_forms)
        return

