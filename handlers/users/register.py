from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from utils import send_req
from loader import dp
from states.personalData import PersonalData, EudcationData
# from keyboards.default.registerKeyBoardButton import reset_password
from aiogram.utils.exceptions import Throttled
from data.config import throttling_time
from pprint import pprint
from datetime import datetime
from handlers.users import collect_data
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

@dp.message_handler(text="🇺🇿O'zbek tili")
async def uz_lang(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_phone = types.KeyboardButton(text='☎️ Telefon raqamni yuborish', request_contact=True)
    keyboard.add(button_phone)
    await message.answer("☎️ Telefon raqamingizni yuboring\nNamuna: 998991234567", reply_markup=keyboard)
    await PersonalData.phone.set()


@dp.message_handler(state=PersonalData.phone, content_types=types.ContentTypes.CONTACT | types.ContentTypes.TEXT)
async def phone_contact_received(message: types.Message, state: FSMContext):
    # await message.answer(message.json())
    # print(message)
    # print(message.text)
    try:
        contact = message.contact
        phone_num = contact.phone_number
        # print('auto:', phone_num)
    except AttributeError:
        phone_num = None
        contact = None
    # print('next')
    try:
        custom_writened_phone = message.text
        # print(custom_writened_phone)
    except AttributeError:
        custom_writened_phone = None
    # print("custom_writened_phone", custom_writened_phone)
    if contact is not None and phone_num is not None:
        custom_phone = f'+{phone_num}'
        # print(phone_num)
        if len(phone_num) == 12:
            # print(phone_num)
            check_user = send_req.check_number(custom_phone)
            # print('check_user', check_user.json())
            if str(check_user.json()) == 'True':

                await state.update_data(phone=phone_num)
                user_login = send_req.user_login(custom_phone)
                # print('user_login: ',user_login)
                if user_login.status_code == 200:
                    remove_keyboard = types.ReplyKeyboardRemove()
                    await message.answer("🟢Telefon raqamingiz qabul qilindi. Telefon raqamingizga yuborilgan kodni kiriting", reply_markup=remove_keyboard)
                    await PersonalData.secret_code.set()

            elif str(check_user.json()) == 'False':
                # print('check_user', check_user)
                await state.update_data(phone_num)
                user_register = send_req.user_register(custom_phone)
                remove_keyboard = types.ReplyKeyboardRemove()
                # print('user_register: ',user_register)
                if user_register.status_code == 201:
                    await message.answer("🟢Telefon raqamingiz qabul qilindi. Telefon raqamingizga yuborilgan kodni kiriting", reply_markup=remove_keyboard)
                    await PersonalData.secret_code.set()

    elif custom_writened_phone is not None:
        custom_writened_phone = custom_writened_phone.strip()
        # print('custom_writened_phone: ',custom_writened_phone)
        status_while = True
        while status_while:
            # print('while ishladi')
            phone_num = custom_writened_phone.strip()
            if len(phone_num) != 12 or not phone_num.isdigit():
                await message.answer("🔴Telefon raqam no\'to\'g\'ri kiritildi!")
                response_msg = await dp.bot.send_message(message.chat.id, "Iltimos, to'g'ri formatda telefon raqamni kiriting.")
                response = await dp.bot.wait_for("message", timeout=20)
                custom_writened_phone = message.text.strip() if response.text else None
                if custom_writened_phone:
                    phone_num = custom_writened_phone
                else:
                    break

            elif len(phone_num) == 12:
                # print('keldi')
                status_while = False
                custom_phone = f'+{phone_num}'
                check_user = send_req.check_number(custom_phone)
                if str(check_user.json()) == 'True':
                    await state.update_data(phone=phone_num)
                    user_login = send_req.user_login(custom_phone)
                    if user_login.status_code == 200:
                        remove_keyboard_ = types.ReplyKeyboardRemove()
                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        reset_pass_button = types.KeyboardButton(text='Kodni qayta yuborish')
                        keyboard.add(reset_pass_button)
                        await message.answer("🟢Telefon raqamingiz qabul qilindi.", reply_markup=remove_keyboard_)
                        await message.answer(" Telefon raqamingizga yuborilgan kodni yuboring", reply_markup=reset_pass_button)
                        await PersonalData.secret_code.set()

                if str(check_user.json()) == 'False':
                    await state.update_data(phone=phone_num)
                    user_register = send_req.user_register(custom_phone)
                    # print('user_register', user_register.json())
                    if user_register.status_code == 201:
                        remove_keyboard_ = types.ReplyKeyboardRemove()
                        # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        # reset_pass_button = types.KeyboardButton(text='reset_password')
                        # keyboard.add(reset_pass_button)
                        await message.answer("🟢Telefon raqamingiz qabul qilindi.", reply_markup=remove_keyboard_)
                        await message.answer("Telefon raqamingizga yuborilgan kodni yuboring")
                        await PersonalData.secret_code.set()

# @dp.message_handler(lambda message: message.text == 'reset_password',state=PersonalData.phone)
# async def reset_password(message: types.Message, state: FSMContext):
#     try:
#         await dp.throttle('reset_password', rate=throttling_time)
#     except Throttled:
#         await message.reply("Sizga tasdiqlash kodi yuborilgan, qayta tasdiqlash kodini 2 daqiqadan so'ng yubora olasiz")
#         return
    
#     data = await state.get_data()
#     phone_number = data.get('phone')
#     token = data.get('token')
#     response = send_req.reset_password(phone=phone_number, token=token)
#     if response.status_code == 200:
#         await message.answer('Yuborilgan tasdiqlash kodini kiriting')




@dp.message_handler(state=PersonalData.secret_code)
async def secret_code(message: types.Message, state: FSMContext):
    # print('secret_code', secret_code)
    # data_user = await state.get_data()
    # token = data_user.get('token')
    status_while = True
    while status_while:
        secret_code = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reset_pass_button = types.KeyboardButton(text='Kodni qayta yuborish')
        keyboard.add(reset_pass_button)
        # print(type(secret_code), 'secret code', secret_code)
        if len(secret_code) == 6 and secret_code.isdigit():
            data = await state.get_data()
            phone_number = f"+{data.get('phone')}"
            # print("phone->", phone_number)
            response_ = send_req.user_verify(int(secret_code), phone_number)
            # print('response', response_.json())
            if response_.status_code == 200:
                data_res = response_.json()
                new_token = data_res.get('token')
                # print("\ndata_res", data_res, '\n')
                await state.update_data(token=data_res.get('token'))
                await state.update_data(last_name=data_res.get('last_name'))
                await state.update_data(first_name=data_res.get('first_name'))
                await state.update_data(avatar=data_res.get('avatar'))
                await state.update_data(haveApplicationForm=data_res.get('haveApplicationForm'))
                await state.update_data(haveApplied=data_res.get('haveApplied'))
                await state.update_data(haveEducation=data_res.get('haveEducation'))
                status_while = False
                # await state.update_data(**data_to_update)
            
            elif response_.status_code == 404 or response_.status_code == 400 or response_.status_code == 410:
                # print('\nres',response_.json(), '\n')
                await message.answer("🔴 Tasdiqlash kodi noto'g'ri kiritildi")
                response_msg = await dp.bot.send_message(message.chat.id, "Tasdiqlash kodini qayta kiriting", reply_markup=reset_pass_button)
                response = await dp.bot.wait_for("message")
                break
        else:
            await message.answer("🔴Tasdiqlash kodi noto'g'ri kiritildi", reply_markup=reset_pass_button)
            break
        status_while = False
        remove_keyboard_ = types.ReplyKeyboardRemove()
        await state.update_data(secret_code=secret_code)
        await message.answer("🟢Kod qabul qilindi")

    serial_number = 'serial_number'
    serial_number_res = collect_data.collect_me_data(token=new_token,field_name=serial_number)
    print('serial_number181: %s' % serial_number_res)
    if serial_number_res is None or serial_number_res == False:
        print('serial_number yoq ekan!!!')
        await message.answer("Passport seriyangizni yuboring\nNamuna: AB1234567", reply_markup=remove_keyboard_)
        await PersonalData.document.set()
    elif serial_number_res is not None:
        print('passport seriya MO bor ekan')
        await PersonalData.info.set()

@dp.message_handler(state=PersonalData.document)
async def document(message: types.Message, state: FSMContext):
    await message.answer('Document qidirilmoqda document')
    # print('document')
    data_user = await state.get_data()
    token = data_user.get('token')
    serial_number = 'serial_number'
    pprint(collect_data.collect_me_data(token))
    serial_number_res = collect_data.collect_me_data(token=token,field_name=serial_number)
    print('serial_number topildi:', serial_number_res)
    if serial_number_res is None or serial_number_res == False:
        document = message.text.strip()
        document_serial = str(document[:2]).upper().strip()
        document_number = document[2:]
        status_while = True
        while status_while:
            if len(document_serial) == 2 and document_serial.isalpha() and len(document_number) == 7 and document_number.isdigit():
                formatted_document = f'{document_serial}{document_number}'
                await state.update_data(document=formatted_document)
                status_while = False
                await PersonalData.birth_date.set()

            elif len(document_serial) == 2 and not document_serial.isalpha():
                await message.answer("🔴Passport seriya noto'g'ri kiritildi")
                response_msg = await dp.bot.send_message(message.chat.id, "Passport seriyasi 2 ta harfdan  va 7 raqamdan iborat bo'lishi kerak.\nQayta passport seriyangizni kiriting")
                response = await dp.bot.wait_for("message")
                custom_writened_passport_serial = message.text.strip() if response.text else None
                if custom_writened_passport_serial:
                    document_serial = custom_writened_passport_serial
                else:
                    break
            elif len(document_number) == 7 and not document_number.isdigit():
                await message.answer("🔴Passport seriya noto'g'ri kiritildi")
                response_msg = await dp.bot.send_message(message.chat.id, "Passport seriyasi 2 ta harfdan va 7 raqamdan iborat bo'lishi kerak.\nQayta passport seriyangizni kiriting")
                response = await dp.bot.wait_for("message")
                custom_writened_document_number = message.text.strip() if response.text else None
                if custom_writened_document_number:
                    document_number = custom_writened_document_number
                else:
                    break
            elif len(document_serial) == 2 and document_serial.isalpha() and len(document_number) != 7:
                await message.answer("🔴Passport seriya noto'g'ri kiritildi")
                reponse_msg = await dp.bot.send_message(message.chat.id,"Passport seriyasi 2 ta harfdan va 7 raqamdan iborat bo'lishi kerak.\nQayta passport seriyangizni kiriting")
                response = await dp.bot.wait_for("message")
                custom_writened_document_serial = message.text.strip() if response.text else None
                if custom_writened_document_serial:
                    document_serial = custom_writened_document_serial
                else:
                    break
        await message.answer("🟢Passport seriyasi qabul qilindi")
        await message.answer('Tug\'ilgan kuningingizni kiriting quidagi formatda\nKun.Oy.Yil')
        await PersonalData.birth_date.set()
    else:
        await PersonalData.info.set()

@dp.message_handler(state=PersonalData.birth_date)
async def birth_date(message: types.Message, state: FSMContext):
    await message.answer('Document qidirilmoqda birth_date')
    print('birth date')
    data_user = await state.get_data()
    token = data_user.get('token')
    birth_date = 'birth_date'
    birth_date_res = collect_data.collect_me_data(token=token,field_name=birth_date)
    print('birth_date_res topildi->', birth_date_res)
    if birth_date_res is None or birth_date_res == False:
        birth_date = message.text.strip()
        # Check if the birth date format is valid
        birth_date_parts = birth_date.split('.') if birth_date else None
        # print('birth_date', birth_date_parts)
        if not birth_date_parts or len(birth_date_parts) != 3:
            await message.answer("🔴 Tug'ilgan kun noto'g'ri kiritildi. Sana formati: Kun.Oy.Yil\nTug'ilgan kunni qayta kiriting")
            return

        check_day, check_month, check_year = birth_date_parts
        if not (check_day.isdigit() and check_month.isdigit() and check_year.isdigit()):
            await message.answer("🔴 Tug'ilgan kun noto'g'ri kiritildi. Sana formati: Kun.Oy.Yil\nTug'ilgan kunni qayta kiriting")
            return

        day, month, year = map(int, birth_date_parts)
        # print(day, month, year)
        if not (1 <= day <= 31 and 1 <= month <= 12 and 2024 > year > 1990):
            await message.answer("🔴 Tug'ilgan kun noto'g'ri kiritildi. Kiritilgan sana tog'ri emas.\nTug'ilgan kunni qayta kiriting")
            return

        await state.update_data(birth_date=birth_date)
        await message.answer('🟢Tu\'gilgan kuningiz qabul qilindi. Ma\'lumotlaringiz muvaffaqiyatli saqlandi.')
        formatted_birth_date = f'{year}-{month}-{day}'
        await state.update_data(formatted_birth_date=formatted_birth_date)
        await message.answer('Siz bilan aloqaga chiqish uchun qo\'shimcha telefon raqam kiriting')
        await PersonalData.info.set()
    else:
        PersonalData.info.set()

@dp.message_handler(state=PersonalData.info)
async def info(message: types.Message, state: FSMContext):
    await message.answer('Q\'shimcha nomeringiz qidirilmoqda info')
    print('extra_phone searching...')
    data_user = await state.get_data()
    token = data_user.get('token')
    extra_phone = 'extra_phone'
    extra_phone_res = collect_data.collect_me_data(token=token,field_name=extra_phone)
    print('extra_phone_res->', extra_phone, extra_phone_res)

    if extra_phone_res is None or extra_phone_res == False:
        extra_phone = message.text.strip()
        # print('extra_phone', extra_phone)
        data = await state.get_data()
        # print('\nstate ga saqlanganlar-->\n', data)
        formatted_birth_date = data.get('formatted_birth_date')
        document = data.get('document')
        token = data.get('token')
        # first_name = data.get('first_name')
        # last_name = data.get('last_name')
        phone = data.get('phone')

        date_obj = datetime.strptime(formatted_birth_date, "%Y-%m-%d")
        formatted_date_str = date_obj.strftime("%Y-%m-%d")

        # print('-->',formatted_date_str,document)
        response = send_req.application_form_info(formatted_date_str,document,token)
        print("response", response.json())
        data_res = response.json().get('passport', {})
    # Default values are used where data might not be present
        first_name = data_res.get('first_name', '')
        last_name = data_res.get('last_name', '')
        application_id = data_res.get('applicant_id', '')  # Note the key is 'applicant_id' based on your response
        third_name = data_res.get('third_name', '')
        document = data_res.get('document', '')
        birth_country = data_res.get('birth_country', '')
        birth_country_id = data_res.get('birth_country_id', 0)
        birth_date = data_res.get('birth_date', '')
        birth_place = data_res.get('birth_place', '')
        citizenship = data_res.get('citizenship', '')
        gender = data_res.get('gender', '')
        photo = data_res.get('photo', '')
        pin = data_res.get('pin', [None])[0]
        document_info = data_res.get('document', {})
        docgiveplace = document_info.get('docgiveplace', '')
        docgiveplaceid = document_info.get('docgiveplaceid', 0)
        datebegin = document_info.get('datebegin', '')
        dateend = document_info.get('dateend', '')
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
        }
        # pprint(user_datas)
        await state.update_data(**user_datas)

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
                                                            document,
                                                            src,
                                                            third_name
                                                            )
        # print(response_application_form.json())
        if response_application_form.status_code == 201:
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
            await message.answer("Ta'lim malumotlarini kiriting")
            await message.answer("Bitirgan yoki tahsil olayotgan ta'lim dargohi turini tanlang")
            await EudcationData.education_id.set()
    else:
        await EudcationData.education_id.set()
    
@dp.message_handler(state=EudcationData.education_id)
async def education_id(message: types.Message, state: FSMContext):
    await message.answer('tanlang education_id')
    print('education_id')
    data = await state.get_data()
    token = data.get("token")
    education_id = "education_id"
    # education_id_res = collect_data.collect_me_data(token=token,field_name=education_id)
    # if education_id_res is None or education_id_res == False:
        # educations_res = send_req.educations(token)
        # array_educations = []
        # for obj in educations_res:
        #     name_uz = obj['name_uz']
        #     name_id = obj['id']
        #     obj = {
        #         'id': name_id,
        #         'name_uz': name_uz
        #     }
        #     array_educations.append(obj)
    obj = [
        {'id': '1', 'name_uz': 'iqtisod'},
        {'id': '2', 'name_uz': 'dizayn'},
        # Add more items as needed
    ]
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for item in obj:
        button_text = item['name_uz']
        callback_data = item['id']
        inline_kb.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    logging.info(message)
    # Sending a message with the inline keyboard
    await message.answer("Choose an option:", reply_markup=inline_kb)


# @dp.callback_query_handler()
# async def handle_callback_query(callback_query: types.CallbackQuery):
#     # Here, you can add your logic to handle different callback data
#     await message.answer_callback_query(callback_query.id)
#     await message.send_message(callback_query.from_user.id, f"You selected ID: {callback_query.data}")






        


