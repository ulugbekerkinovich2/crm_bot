from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.default.registerKeyBoardButton import menu, application, ask_delete_account,exit_from_account, update_personal_info,finish_edit,update_education_info
from keyboards.inline.menukeyboards import update_personal_info_inline,edit_user_education_inline,edit_user_education_transfer_inline
from states.personalData import PersonalData, UpdateMenu,UpdateEducation,EducationData
from loader import dp
from utils import send_req
from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic
from data.config import domain_name
from datetime import datetime
import aiofiles.os
import os
import pytz
import json
from data.config import username as USERNAME
from data.config import password as PASSWORD
from handlers.users import upload,collect_data
from handlers.users.register import saved_message,select_region,type_your_edu_name,example_diploma_message,wait_file_is_loading,select_type_certificate,example_certification_message,not_found_country,search_university,select_one
start_button = KeyboardButton('/start')  # The text on the button
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)
escape_markdown = send_req.escape_markdown
convert_time = send_req.convert_time
@dp.message_handler(Text(equals="🗑Akkauntni o'chirish"), state="*")
async def delete_account_prompt(message: types.Message, state: FSMContext):
    await message.answer("Akkaunt o'chirilsinmi?", reply_markup=ask_delete_account)

@dp.message_handler(Text(equals="Ha, akkauntni o'chirish"), state="*")
async def delete_account(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    delete_account_result = await send_req.delete_profile(token)
    ic(delete_account_result)
    if delete_account_result == 200:
        await state.update_data(start_count=0)
        response_message = "Sizning akkauntingiz muvaffaqiyatli o'chirildi."
    else:
        response_message = f"Xatolik yuz berdi: {delete_account_result.get('error')}"
    await state.update_data(token=None)
    await message.answer(response_message, reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(state=EducationData.menu)
# async def show_menu(message: Message):
#     await message.answer("Akkauntga hush kelibsiz!", reply_markup=menu)


@dp.message_handler(Text(equals="Akkauntdan chiqish"), state="*")
async def ask_exit_menu(message: Message, state: FSMContext):
    await message.answer("Akkauntdan chiqishni istaysizmi?", reply_markup=exit_from_account)

@dp.message_handler(Text(equals="Ha, Akkauntdan chiqish"), state="*")
async def exit_menu(message: Message, state: FSMContext):
    await state.update_data(token=None)
    await state.update_data(start_count=0)
    await message.answer('Siz akkauntdan chiqdingiz\nStart tugmasini bosib qaytadan tizimga kiring', reply_markup=start_keyboard)

@dp.message_handler(Text(equals="Bekor qilish"), state="*")
async def stay_menu(message: Message, state: FSMContext):
    await message.answer("Asosiy sahifa", reply_markup=menu)

@dp.message_handler(Text(equals="ℹ️Shaxsiy ma'lumotlarim"), state="*")
async def my_menu(message: Message, state: FSMContext):
    ic('Quidagi amallarni bajarishingiz mumkin')
    await message.answer("Quidagi amallarni bajarishingiz mumkin", reply_markup=update_personal_info)


@dp.message_handler(Text(equals="📄Shaxsiy ma'lumotlarni ko'rish"), state="*")
async def my_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    ic(66)
    token = data.get('token')
    ic(token)
    ic(74)
    if token:
        ic('token mavjud, shaxsiy ma\'lumotlarni ko\'rish', token)
        personal_info = await send_req.application_forms_me(token)
        
        photo = f"https://{domain_name}/{personal_info['photo']}" if f"https://{domain_name}/{personal_info['photo']}" else 'rasm topilmadi'
        ic(photo)
        
        first_name = personal_info['first_name'] if personal_info['first_name'] else 'ism topilmadi'
        last_name = personal_info['last_name'] if personal_info['last_name'] else 'familiya topilmadi'
        third_name = personal_info['third_name'] if personal_info['third_name'] else 'otasini ismi topilmadi'
        serial_number = personal_info['serial_number'] if personal_info['serial_number'] else 'seriya va raqami topilmadi'
        birth_date = send_req.convert_time(personal_info['birth_date'])  if send_req.convert_time(personal_info['birth_date']) else 'tugilgan sanasi topilmadi'
        pin = personal_info['pin'] if personal_info['pin'] else "JSHSHR topilmadi"
        gender = 'erkak' if personal_info.get('gender') == 'male' else 'ayol' if personal_info.get('gender') == 'female' else 'jins topilmadi'

        citizenship = personal_info['citizenship'] if personal_info['citizenship'] else "O'zbekiston Respublikasi"
        birth_place = personal_info['birth_place'] if personal_info['birth_place'] else 'tug\'ilgan joyi topilmadi'
        phone = personal_info['phone'] if personal_info['phone'] else 'telefon raqami topilmadi'
        extra_phone = personal_info['extra_phone'].replace(" ", "") if personal_info['extra_phone'] else 'qo\'shimcha telefon raqami topilmadi'
        info_message = (
        "<b>Shaxsiy Ma'lumotlar:</b>\n\n"
        f"• <b>Ism:</b> {first_name}\n"
        f"• <b>Familiya:</b> {last_name}\n"
        f"• <b>Otasi ismi:</b> {third_name}\n"
        f"• <b>Seriya va raqami:</b> {serial_number}\n"
        f"• <b>Tug'ilgan sanasi:</b> {birth_date}\n"
        f"• <b>JSHSHR:</b> {pin}\n"
        f"• <b>Jins:</b> {gender}\n"
        f"• <b>Fuqarolik:</b> {citizenship}\n"
        f"• <b>Tug'ilgan joyi:</b> {birth_place}\n"
        f"• <b>Telefon raqami:</b> {phone}\n"
        f"• <b>Qo'shimcha telefon raqami:</b> {extra_phone}\n"
        )
        await message.answer_photo(photo, caption=info_message, reply_markup=menu, parse_mode="HTML")
    else:
        await message.answer('Profil ma\'lumotlari topilmadi\nStart tugmasini bosib qaytadan tizimga kiring', reply_markup=start_keyboard)

@dp.message_handler(Text(equals="📝Shaxsiy ma'lumotlarni tahrirlash"), state="*")
async def my_menu(message: Message, state: FSMContext):
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
                                                        pin=1,date=date, username=username)
    ic(save_chat_id)

    get_this_user = send_req.get_user_profile(chat_id=user_chat_id)
    ic(get_this_user)
    data = await state.get_data()
    token = data.get('token')
    # update_personal_info_inline_dict = update_personal_info_inline.to_dict()
    # # Convert dictionary to JSON string
    # update_personal_info_inline_json = json.dumps(update_personal_info_inline_dict)
    await message.answer('Qaysi ma\'lumotingizni tahrirlamoqchisiz',
                          reply_markup=update_personal_info_inline)
    await UpdateMenu.firstname.set()





@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata, state=UpdateMenu.firstname)
async def update_personal_info_hand(callback_query: types.CallbackQuery, state: FSMContext):
    my_callback = callback_query.data
    ic(my_callback)
    await state.update_data(callback=my_callback)
    my_obj = {
        'firstname': 'Yangilamoqchi bo\'lgan ismni kiriting: ',
        'lastname': 'Yangilamoqchi bo\'lgan familiyani kiriting',
        'thirdname': 'Yangilamoqchi bo\'lgan otangizni ismini kiriting',
        'passport': 'Yangilamoqchi bo\'lgan Passport seriya raqamini kiriting, Quidagi formatda kiriting: AB1234567',
        'birthdate': 'Yangilamoqchi bo\'lgan tug\'ilgan kuningizni kiriting, Quidagi formatda kiriting: yyyy-oo-kk',
        'gender': 'Yangilamoqchi bo\'lgan jinsni kiriting, Quidagi formatda kiriting: Erkak/Ayol',
        'birthplace': 'Yangilamoqchi bo\'lgan tug\'ilgan joyingizni kiriting, Namuna: Toshkent shahri',
        'extra_phone': 'Yangilamoqchi bo\'lgan qo\'shimcha telefon raqamingizni kiriting, Namuna: +998991234567',
    }
    res_mess = my_obj.get(my_callback)
    await callback_query.message.answer(res_mess)
    await UpdateMenu.lastname.set()

@dp.message_handler(state=UpdateMenu.lastname)
async def get_user_input(message: types.Message, state: FSMContext):
    
    user_input = message.text
    if user_input == "📚 Ta'lim ma'lumotlarni ko'rish" or user_input == "📚Ta'lim ma'lumotlarim":
        return
    ic(user_input)
    data = await state.get_data()
    get_callback = data.get('callback')
    ic(143, get_callback)
    token = data.get('token')
    date_me = await send_req.application_forms_me(token)
    ic(date_me)
    birth_place = user_input if get_callback == 'birthplace' else date_me.get('birth_place', ' ')
    birth_date = user_input if get_callback == 'birthdate' else date_me.get('birth_date', ' ')
    citizenship = user_input if get_callback == 'citizenship' else date_me.get('citizenship', ' ')
    extra_phone = user_input if get_callback == 'extra_phone' else date_me.get('extra_phone', ' ')
    first_name = user_input if get_callback == 'firstname' else date_me.get('first_name', ' ')
    # gender = user_input if get_callback == 'gender' else date_me.get('gender', ' ')
    if get_callback == 'gender':
        if user_input == 'Erkak':
            gender = 'male'
        else:
            gender = 'female'
    else:
        gender = date_me.get('gender', ' ')
    last_name = user_input if get_callback == 'lastname' else date_me.get('last_name', ' ')

    ic('last_name', last_name)
    
    phone = user_input if get_callback == 'phone' else date_me.get('phone', ' ')
    serial_number = user_input if get_callback == 'passport' else date_me.get('serial_number', ' ')
    src = user_input if get_callback == 'src' else date_me.get('src', ' ')
    third_name = user_input if get_callback == 'thirdname' else date_me.get('third_name', ' ')
    await state.update_data(birth_place=birth_place, birth_date=birth_date, citizenship=citizenship, extra_phone=extra_phone,
                            first_name=first_name, gender=gender, last_name=last_name, phone=phone, serial_number=serial_number,
                            src=src, third_name=third_name)
    await state.update_data(token=token)
    update_user_info = send_req.application_forms_for_personal_data(token,
                                                                    birth_date,
                                                                    birth_place,
                                                                    citizenship,
                                                                    extra_phone,
                                                                    first_name,
                                                                    gender,
                                                                    last_name,
                                                                    phone,
                                                                    serial_number,
                                                                    third_name)

    ic(update_user_info)
    await message.answer(saved_message)
    await UpdateMenu.firstname.set()


@dp.message_handler(Text(equals="📚Ta'lim ma'lumotlarim"), state="*")
async def education_menu(message: Message, state: FSMContext):
    try:
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
                                                            pin=1,date=date, username=username)
        ic(save_chat_id)

        get_this_user = send_req.get_user_profile(chat_id=user_chat_id)
        ic(get_this_user)
    except Exception as err:
        ic(err)

    await message.answer("Quidagilardan birini tanlang", reply_markup=update_education_info)

@dp.message_handler(Text(equals="📝 Ta'lim ma'lumotlarni tahrirlash"), state="*")
async def edit_education_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    transfer_user = data.get('transfer_user')
    register_user = data.get('register_user')
    # haveEducation = data.get('haveEducation')
    # ic('tahrirlash', data)
    ic(transfer_user)
    ic(register_user)
    personal_info = await send_req.application_forms_me(token)
    pnfl_user_education = personal_info.get('pnfl_user_education', {})
    user_education = personal_info.get('user_education', {})
    user_previous_education = personal_info.get('user_previous_education', {})
    haveEducation = personal_info.get('haveEducation', False)
    ic(217, user_previous_education)
    ic(218, haveEducation)
    if token and haveEducation:
        ic(219, user_education )

        # if pnfl_user_education.get('degree_id', None) is None:
        #     if user_education.get('education_id', None) is not None:
        if user_education is not None:

            education_id = user_education.get('education_id')
            education_type_uz = user_education.get('education_type_uz', None)
            region_id = user_education.get('region_id', None)
            region_name_uz = user_education.get('region_name_uz', None)
            district_id = user_education.get('district_id', None)
            district_name_uz = user_education.get('district_name_uz', None)
            file_diploma = user_education.get('file_diploma', None)
            institution_name = user_education.get('institution_name', None)

            await state.update_data(
            education_id=education_id,              
            education_type_uz=education_type_uz, 
            region_id=region_id,
            region_name_uz=region_name_uz,
            district_id=district_id,
            district_name_uz=district_name_uz
            )
            await message.answer("Qaysi ma\'lumotingizni tahrirlamoqchisiz",
                                    reply_markup=edit_user_education_inline)
            await UpdateEducation.education_id.set()
    elif token and user_previous_education is not None:
        ic(246, user_previous_education)
        data_me = await send_req.application_forms_me(token)
        user_previous_education = data_me.get('user_previous_education', {})
        # ic()
        country_id = user_previous_education.get('country_id', None)
        country_name_uz = user_previous_education.get('country_name_uz', None)
        institution_name = user_previous_education.get('institution_name', None)
        transcript_file = user_previous_education.get('transcript_file', None)
        which_course_now = user_previous_education.get('which_course_now', None)
        direction_name = user_previous_education.get('direction_name', None)
        await state.update_data(country_id=country_id, country_name_uz=country_name_uz, institution_name=institution_name, transcript_file=transcript_file, which_course_now=which_course_now)
        await PersonalData.country_search.set()
        ic('perevod uchun keldi')
        await message.answer("Qaysi ma\'lumotingizni tahrirlamoqchisiz",reply_markup=edit_user_education_transfer_inline)

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'country_id', state=EducationData.country_search)
async def education_id_handler(message: types.Message, state: FSMContext, page: int = 0):
    ic('education ga keldi')
    data = await state.get_data()
    token = data.get('token')
    register_user = data.get('register_user')
    transfer_user = data.get('transfer_user')
    ic('register_user', register_user, 'transfer_user', transfer_user)

    if transfer_user:
        # await message.answer(search_university, reply_markup=ReplyKeyboardRemove())
        # ic('shu yerda')
        # Ask user to input the search query for countries
        await PersonalData.country_search.set()  # Assuming country_search is a state for inputting country search
        

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'country_id', state=PersonalData.country_search)
async def education_id_handler(callback_query: types.CallbackQuery, state: FSMContext, page: int = 0):
    ic('shu yer ekan')
    await callback_query.message.answer(search_university, reply_markup=ReplyKeyboardRemove())
    await PersonalData.country_search.set()

@dp.message_handler(lambda message: message.text in ["📚 Ta'lim ma'lumotlarni ko'rish", "📝 Ta'lim ma'lumotlarni tahrirlash"],state=PersonalData.country_search)
async def handle_education_options(message: types.Message, state: FSMContext):
    # Direct handling for specific commands
    # Redirect to appropriate handlers or reset state based on the command
    if message.text == "📚 Ta'lim ma'lumotlarni ko'rish":
        data = await state.get_data()
        ic('keldi700', data)
        token = data.get('token')
        me_data = await send_req.application_forms_me(token)
        haveApplicationForm = me_data.get('haveApplicationForm')
        haveApplied = me_data.get('haveApplied')
        haveEducation = me_data.get('haveEducation')
        havePreviousEducation = me_data.get('havePreviousEducation')
        
        # haveApplicationForm = data.get('haveApplicationForm')
        # haveApplied = data.get('haveApplied')
        # haveEducation = data.get('haveEducation')
        # havePreviousEducation = data.get('havePreviousEducation')
        register_user = data.get('register_user')
        transfer_user = data.get('transfer_user')

        if token and haveEducation:
            education_info = await send_req.application_forms_me(token)
            ic(education_info)
            user_education = education_info.get('user_education', {})
            certifications = education_info.get('certifications', [])
            pinfl_user_education = education_info.get('pinfl_user_education', {})
            # ic(education_info)
            # ic(certifications)
            # ic(pinfl_user_education)
            # ic(user_education)
            education_message = "<b>📚 Ta'lim Ma'lumotlari:</b>\n\n"
            # Constructing the education message
            if education_info.get('user_education_src', None) == 'automatic':
                # ic(education_info.get('user_education_src', None))
                ic('keldi 348')
                education_message += (
                    f"• <b>Ta'lim turi:</b> {user_education.get('education_type_uz', 'Talim turi topilmadi')}\n"
                    f"• <b>Viloyat:</b> {user_education.get('region_name_uz', 'Viloyat topilmadi')}\n"
                    f"• <b>Tuman:</b> {user_education.get('district_name_uz', 'Tuman topilmadi')}\n"
                    f"• <b>O'quv muassasasi nomi:</b> {user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
                )
            elif education_info['user_education_src'] != 'automatic':
                # ic(education_info['user_education_src'])
                ic('keldi 357')
                education_message += (
                    f"• <b>Daraja:</b> {pinfl_user_education.get('degree_name_uz', 'Daraja topilmadi')}\n"
                    f"• <b>Tamomlagan yil:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Tamomlagan yil topilmadi')}\n"
                    f"• <b> Mamlakat:</b> {pinfl_user_education.get('country', 'Shahar topilmadi')}\n"
                    f"• <b>Shahar:</b> {pinfl_user_education.get('region', 'Shahar nomi topilmadi')}\n"
                    f"• <b>Tuman:</b> {pinfl_user_education.get('district', 'Tuman nomi topilmadi')}\n"
                    f"• <b>Ta'lim turi:</b> {pinfl_user_education.get('institution_type', 'Talim turi topilmadi')}\n"
                    f"• <b>O'quv muassasasi nomi:</b> {pinfl_user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
                    f"• <b>Diplom yoki shahodatnoma raqami:</b> {pinfl_user_education.get('document', 'Diplom yoki shahodatnoma raqami topilmadi')}\n"
                )

            # Sending the educational info message
            await message.answer(education_message, parse_mode="HTML", reply_markup=menu)

            diploma_file = user_education.get('file')
            if diploma_file is not None:
                try:
                    await message.answer_document(f"https://{domain_name}/{diploma_file[0]}", caption="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli")
                except Exception as e:
                    print(f"Failed to send diploma file: {e}")
                    await message.answer(chat_id=message.chat.id, text="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli topilmadi, Qayta yuklang")

            elif pinfl_user_education['file'][0] is not None:
                try:
                    await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli")
                except Exception as e:
                    print(f"Failed to send diploma file: {e}")
                    await message.answer(chat_id=message.chat.id, text="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli topilmadi, Qayta yuklang")

                
            # Sending certification files if available

            ic(398)
            if certifications:
                for certification in certifications:
                    if certification.get('file'):
                        ic(127)
                        certification_type = certification.get('certification_type', 'Sertifikat turi topilmadi')
                        try:
                            await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Sertifikat nusxasi: {certification_type.upper()}")
                        except Exception as e:
                            print(f"Failed to send certification file: {e}")   
                            await message.answer(chat_id=message.chat.id, text=f"Sertifikat nusxasi: {certification_type.upper()} topilmadi, Qayta yuklang")
        elif token and havePreviousEducation:
            ic('mytoken', token)
            education_info = await send_req.application_forms_me(token)
            ic(education_info)
            user_education = education_info.get('user_previous_education', None)
            pinfl_user_education = education_info.get('pinfl_user_education', {})

            certifications = education_info.get('certifications', [])
            if user_education is not None:
                education_message = "<b>📚 Ta'lim Ma'lumotlari:</b>\n\n"
                education_message += (
                    f"• <b>Mamlakat:</b> {user_education.get('country_name_uz', 'Viloyat topilmadi')}\n"
                    f"• <b>O'quv muassasasi nomi:</b> {user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
                    f"""• <b>Yo'nalish:</b> {user_education.get('direction_name', "Yonalish topilmadi")}\n"""
                    f"• <b>Kurs:</b> {user_education.get('which_course_now', 'Daraja topilmadi')}-chi kurs\n"
                )
                
                if pinfl_user_education is not None:
                    if pinfl_user_education['pinfl_region_id'] is not None:
                        education_message += (
                            f"• <b>Daraja:</b> {pinfl_user_education.get('degree_name_uz', 'Daraja topilmadi')}\n"
                            f"• <b>Tamomlagan yil:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Tamomlagan yil topilmadi')}\n"
                            f"• <b> Mamlakat:</b> {pinfl_user_education.get('country', 'Shahar topilmadi')}\n"
                            f"• <b>Shahar:</b> {pinfl_user_education.get('region', 'Shahar nomi topilmadi')}\n"
                            f"• <b>Tuman:</b> {pinfl_user_education.get('district', 'Tuman nomi topilmadi')}\n"
                            f"• <b>Ta'lim turi:</b> {pinfl_user_education.get('institution_type', 'Talim turi topilmadi')}\n"
                            f"• <b>O'quv muassasasi nomi:</b> {pinfl_user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
                    )
                await message.answer(education_message, parse_mode="HTML", reply_markup=menu)

                transcript_file = user_education.get('transcript_file')
                if transcript_file:
                    try:
                        await message.answer_document(f"https://{domain_name}/{transcript_file}", caption="Transkript nusxasi fayli")
                    except Exception as e:
                        print(f"Failed to send diploma file: {e}")
                        await message.answer(chat_id=message.chat.id, text="Transkript nusxasi fayli topilmadi, Qayta yuklang")
                elif pinfl_user_education:
                    try:
                        await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli")
                    except Exception as e:
                        print(f"Failed to send diploma file: {e}")
                        await message.answer(chat_id=message.chat.id, text="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli topilmadi, Qayta yuklang")
                    
                # Sending certification files if available

                ic(124)
                if certifications is not None and certifications:
                    for certification in certifications:
                        if certification.get('file'):
                            ic(127)
                            certification_type = certification.get('certification_type', 'Sertifikat turi topilmadi')
                            try:
                                await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Sertifikat nusxasi: {certification_type.upper()}")
                            except Exception as e:
                                print(f"Failed to send certification file: {e}") 
                                await message.answer(chat_id=message.chat.id, text="Sertifikat nusxasi fayli topilmadi, Qayta yuklang")
        else:

            # Handle the case where the token is None or invalid
            await message.answer("Kechirasiz, sizning ma'lumotlaringizni olish imkoni bo'lmadi. Iltimos, akkauntdan chiqib qayta tizimga kiring.")
        # Example: Navigate to viewing educational data
        # await message.answer("📚 Ta'lim ma'lumotlari", reply_markup=update_education_info)
    # elif message.text == "📝 Ta'lim ma'lumotlarni tahrirlash":
    #     # Example: Navigate to editing educational data
    #     await message.answer("📝 Ta'lim ma'lumotlarni tahrirlash", reply_markup=)
    # await state.reset_state() 

@dp.message_handler(Text(equals=["📁Arizam","📁arizam"]), state=PersonalData.country_search)
async def my_application(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    ic('keldi arizaga')
    my_app = await send_req.my_applications(token=token)
    if not my_app:
        await message.answer("Ariza ma'lumotlari topilmadi.")
        return

    created_at = my_app.get('created_at', 'yaratilgan vaqti topilmadi')
    status = my_app.get('status', 'status topilmadi')
    direction_name_uz = my_app.get('direction_name_uz', 'Talim turi topilmadi')
    degree_name_uz = my_app.get('degree_name_uz', 'Talim darajasi topilmadi')
    education_type_name_uz = my_app.get('education_type_name_uz','Talim turi topilmadi' )
    education_language_name_uz = my_app.get('education_language_name_uz', 'Talim tili topilmadi')
    tuition_fee = my_app.get('tuition_fee', 'Narxi topilmadi')
    comments = my_app.get('comment', 'Izoh topilmadi')
    date_obj = datetime.fromisoformat(created_at.rstrip("Z"))
    utc_timezone = pytz.timezone('UTC')
    desired_timezone = pytz.timezone('Asia/Tashkent')  # Replace 'Asia/Tashkent' with your desired timezone
    date_obj = utc_timezone.localize(date_obj).astimezone(desired_timezone)
    human_readable_date = date_obj.strftime("%Y-%m-%d %H:%M")
    if len(comments) >= 2:
        comments = comments[-1]
    
    if tuition_fee != 'Narxi topilmadi':
        formatted_fee = "{:,.0f}".format(tuition_fee).replace(',', '.')
    ic(status)
    applicant_status_translations = {
    'PENDING': 'kutilmoqda',
    'ACCEPTED': 'qabul qilingan',
    'REJECTED': 'rad etilgan',
    'EDIT-REJECT': 'tahrirlash uchun ariza rad etildi',
    'CALLED-EXAM': 'imtihonga chaqirilgan',
    'EXAM-FEE': 'imtihon uchun to\'lov to\'langan',
    'CAME-EXAM': 'imtihonga kelgan',
    'MARKED': 'baholangan',
    'SUCCESS': 'muvaffaqiyatli',
    'FAIL': 'muvaqqiyatsiz',
    'CONTRACT': 'shartnoma',
    'STUDENT': 'talaba',
    'RECOMMENDED_STUDENT': 'tavsiya etilgan talaba'
    }
    status_name = applicant_status_translations.get(status.upper(), "Topilmadi")
    comment = comments.get('comment', 'Izoh topilmadi')
    comment_time = comments.get('created_at', 'Izoh topilmadi')
    if comment_time != 'Izoh topilmadi':
        comment_time = datetime.fromisoformat(comment_time.rstrip("Z")).strftime("%Y-%m-%d %H:%M")
    ic(my_app.get('status'))
    response_message = (
        f"<b>Ariza Tafsilotlari:</b>\n"
        f"Yaratilgan vaqti: {human_readable_date}\n"
        f"Holati:   <b>{status_name}</b>\n"
        f"Yo'nalishi: {direction_name_uz}\n"
        f"Darajasi: {degree_name_uz}\n"
        f"Ta'lim turi: {education_type_name_uz}\n"
        f"Ta'lim til: {education_language_name_uz}\n"
        f"Ta'lim narix: {formatted_fee} so'm\n"
        f"Izoh vaqti: {comment_time}\n"
        f"Izoh: {comment}"
    )
    await message.answer(response_message, parse_mode='HTML')

@dp.message_handler(state=PersonalData.country_search)
async def process_country_search(message: types.Message, state: FSMContext):
    ic("keldi 268")
    user_query = message.text.lower()
    if user_query in ["📚 Ta'lim ma'lumotlarni ko'rish", "📝 Ta'lim ma'lumotlarni tahrirlash","📁arizam",
                      "📁Arizam"]:
        await PersonalData.country_search.set()
        return
    ic('user_query', user_query)
    token = (await state.get_data()).get('token')
    all_countries = await send_req.countries(token)  # Ensure this is an async call to your backend/API

    matching_countries = [country for country in all_countries if user_query in country['name_uz'].lower()]
    
    if not matching_countries:
        await message.answer(not_found_country)
        return

    buttons = [
        [InlineKeyboardButton(text=country['name_uz'], callback_data=f"country_{country['id']}")]
        for country in matching_countries
    ]
    country_menu = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(select_one, reply_markup=country_menu)
    await PersonalData.country_search.set()
    # await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('country_'), state=PersonalData.country_search)
async def handle_country_selection(callback_query: types.CallbackQuery,state: FSMContext):
    await callback_query.answer()  
    selected_country_id = callback_query.data.split('_')[1]
    ic('selected_country_id',selected_country_id)
    await state.update_data(country_id=selected_country_id)
    data = await state.get_data()
    token = data.get('token')
    ic(454, data)
    me_data = await send_req.application_forms_me(token)
    user_previous_education = me_data.get('user_previous_education', {})
    country_id = user_previous_education.get('country_id')
    # country_name_uz = me_datadata.get('country_name_uz')
    institution_name = user_previous_education.get('institution_name', None)
    transcript_file = user_previous_education.get('transcript_file', None)
    which_course_now = user_previous_education.get('which_course_now', None)
    direction_name = user_previous_education.get('direction_name', None)
    application_forms_transfer = await send_req.application_forms_transfer(token, 
                                                                           int(selected_country_id),
                                                                           direction_name,
                                                                        institution_name, 
                                                                        transcript_file, 
                                                                        which_course_now
                                                                        )
    ic(application_forms_transfer)
    await callback_query.message.answer(saved_message, reply_markup=update_education_info)



@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'institution_name', state=PersonalData.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    
    await call.message.answer("Ta'lim dargohi nomini kiriting", reply_markup=update_education_info)
    await PersonalData.transfer_edu_name.set()

@dp.message_handler(state=PersonalData.transfer_edu_name)
async def update_education(message: types.Message, state: FSMContext):
    inst_name = message.text.strip()
    ic(inst_name)
    # if message_text in ["📚 Ta'lim ma'lumotlarni ko'rish", "📝 Ta'lim ma'lumotlarni tahrirlash"]:
    #     return
    data = await state.get_data()
    ic(data)
    token = data.get('token')
    me_data = await send_req.application_forms_me(token)
    user_previous_education = me_data.get('user_previous_education', {})

    country_id = user_previous_education.get('country_id', None)
    transfer_direction_name = user_previous_education.get('direction_name', None)
    # transfer_education_name = user_previous_education.get('institution_name', None)
    file_diploma_transkript = user_previous_education.get('file_diploma_transkript', None)
    which_course_now = user_previous_education.get('which_course_now', None)

    application_forms_transfer = await send_req.application_forms_transfer(
        token=token,
        country_id=int(country_id),
        direction_name=transfer_direction_name,
        institution_name=inst_name,
        transcript_file=file_diploma_transkript,
        which_course_now=int(which_course_now)
    )
    await message.answer(saved_message, reply_markup=update_education_info)
    ic(application_forms_transfer)
    await state.update_data(institution_name=inst_name)
    await PersonalData.country_search.set()

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'direction_name', state=PersonalData.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ta’lim yo’nalishi nomini kiriting:", reply_markup=update_education_info)
    await PersonalData.transfer_direction_name.set()

@dp.message_handler(state=PersonalData.transfer_direction_name)
async def update_education(message: types.Message, state: FSMContext):
    direction_name = message.text.strip()
    ic(direction_name)
    data = await state.get_data()
    token = data.get('token')

    me_data = await send_req.application_forms_me(token)
    user_previous_education = me_data.get('user_previous_education', {})

    country_id = user_previous_education.get('country_id', None)
    # transfer_direction_name = user_previous_education.get('direction_name', None)
    transfer_education_name = user_previous_education.get('institution_name', None)
    file_diploma_transkript = user_previous_education.get('file_diploma_transkript', None)
    which_course_now = user_previous_education.get('which_course_now', None)

    application_forms_transfer = await send_req.application_forms_transfer(
        token=token,
        country_id=int(country_id),
        direction_name=direction_name,
        institution_name=transfer_education_name,
        transcript_file=file_diploma_transkript,
        which_course_now=int(which_course_now)
    )
    await state.update_data(direction_name=direction_name)
    await message.answer(saved_message, reply_markup=update_education_info)
    await PersonalData.country_search.set()

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'current_course', state=PersonalData.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Yangilamoqchi bo'lgan kursingizni kiriting: Namuna 1 yoki 2", reply_markup=update_education_info)
    await PersonalData.current_course.set()

@dp.message_handler(state=PersonalData.current_course)
async def update_education(message: types.Message, state: FSMContext):
    current_course = message.text.strip()
    ic(current_course)
    data = await state.get_data()
    token = data.get('token')

    me_data = await send_req.application_forms_me(token)
    user_previous_education = me_data.get('user_previous_education', {})

    country_id = user_previous_education.get('country_id', None)
    transfer_direction_name = user_previous_education.get('direction_name', None)
    transfer_education_name = user_previous_education.get('institution_name', None)
    file_diploma_transkript = user_previous_education.get('file_diploma_transkript', None)
    # which_course_now = user_previous_education.get('which_course_now', None)

    application_forms_transfer = await send_req.application_forms_transfer(
        token=token,
        country_id=int(country_id),
        direction_name=transfer_direction_name,
        institution_name=transfer_education_name,
        transcript_file=file_diploma_transkript,
        which_course_now=int(current_course)
    )
    await state.update_data(direction_name=transfer_direction_name)
    await message.answer(saved_message, reply_markup=update_education_info)
    await PersonalData.country_search.set()


@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'transcript', state=PersonalData.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Yangilamoqchi bo'lgan Transkript nusxasini yuboring:", reply_markup=update_education_info)
    await PersonalData.transcript.set()


@dp.message_handler(content_types=['document'], state=PersonalData.transcript)
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
    await message.answer(wait_file_is_loading, parse_mode='HTML')
    # ic(local_file_path)

    res_file = upload.upload_new_file_transcript(token=token_, filename=local_file_path)
    # if file_size != 'File not found':
    try:
        file_size = os.path.getsize(local_file_path)
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024
        ic(f'size: {file_size_mb:.2f}')
    except: 
        return 'File not found'
    await state.update_data(file_size=file_size)
    await message.answer("Fayl yuklandi.")
    
    # ic(all_state)
    # print(res_file.status_code)
    # print(res_file)
    try:
        data1 = res_file.json()
        path = data1['path']
        ic(path)
        data = await state.get_data()
        # file_diploma_transkript = path
        # country_id = data.get('country_id')
        # selected_course = data.get('selected_course')
        # transfer_direction_name = data.get('transfer_direction_name')
        # transfer_education_name = data.get('transfer_education_name')
        # res_data = await send_req.application_forms_transfer(
        #     token_,
        #     int(country_id),
        #     transfer_direction_name,
        #     transfer_education_name,
        #     file_diploma_transkript,
        #     int(selected_course)
        # )
        # ic(res_data)
        token = data.get('token')
        me_data = await send_req.application_forms_me(token)
        user_previous_education = me_data.get('user_previous_education', {})

        country_id = user_previous_education.get('country_id', None)
        transfer_direction_name = user_previous_education.get('direction_name', None)
        transfer_education_name = user_previous_education.get('institution_name', None)
        # file_diploma_transkript = user_previous_education.get('file_diploma_transkript', None)
        which_course_now = user_previous_education.get('which_course_now', None)

        application_forms_transfer = await send_req.application_forms_transfer(
            token=token,
            country_id=int(country_id),
            direction_name=transfer_direction_name,
            institution_name=transfer_education_name,
            transcript_file=path,
            which_course_now=int(which_course_now)
         )
        await message.answer(saved_message, reply_markup=update_education_info)
        await state.update_data(file_diploma_transkript=path)
        
    except Exception as e:
        ic(e)
        await message.answer(e)
        return e
    await PersonalData.country_search.set()


@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'education', state=UpdateEducation.education_id)
async def update_education(call: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN  
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    data = await state.get_data()
    token = data.get('token')
    educations_response = send_req.educations(token) 
    educations = educations_response.json()  
    
    buttons = [[InlineKeyboardButton(text=item['name_uz'], callback_data=f"edu_{item['id']}")] for item in educations]
    educationMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(call.from_user.id,"<b>Bitirgan yoki tahsil olayotgan ta'lim dargohi turini tanlang:</b>", parse_mode='HTML',reply_markup=educationMenu)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('edu_'), state=UpdateEducation.education_id)
async def update_education_handler(callback_query: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    data_call = callback_query.data
    ic(data_call)
    education_id_call = int(callback_query.data.split('edu_')[1])
    ic(education_id_call)

    data = await state.get_data()
    token = data.get('token')
    ic(258, token)

    data_me = await send_req.application_forms_me(token)

    user_education = data_me.get('user_education', {})
    if user_education:
        # education_id = user_education.get('education_id', None)
        district_id =  user_education.get('district_id', None)
        region_id = user_education.get('region_id', None)
        institution_name = user_education.get('institution_name', None)
        src = user_education.get('src', None)
        region_id = user_education.get('region_id', None)
        file_diploma = user_education.get('file', None)
        await state.update_data(education_id=education_id_call, district_id=district_id, region_id=region_id, institution_name=institution_name, src=src, file_diploma=file_diploma[0])
    new_data = await state.get_data()
    district_id_= new_data.get('district_id')
    education_id_ = new_data.get('education_id')
    region_id_ = new_data.get('region_id')
    institution_name_ = new_data.get('institution_name')
    src_ = new_data.get('src')
    file_diploma_ = new_data.get('file_diploma')
    update_education = send_req.application_forms_for_edu(token,district_id_,
                                                                education_id_,
                                                                file_diploma_,
                                                                institution_name_,
                                                                region_id_,
                                                                src_)
    
    # update_education_info = update_education.json()
    # ic(259, update_education.json())
    # ic(260, data_me)
    await state.update_data(education_id=education_id_call)
    await callback_query.answer()
    await UpdateEducation.region_id.set()
    await bot.send_message(callback_query.from_user.id, saved_message, parse_mode="HTML", reply_markup=update_education_info)

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'region', state=UpdateEducation.education_id)
async def update_region(callback_query: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    data = await state.get_data()
    token = data['token']
    region_response = send_req.regions(token)
    regions = region_response.json()
    buttons = [[InlineKeyboardButton(text=item['name_uz'], callback_data=f"reg_{item['id']}")] for item in regions]
    regionMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(callback_query.from_user.id,select_region, reply_markup=regionMenu)

@dp.callback_query_handler(lambda c: c.data.startswith('reg_'),state=UpdateEducation.education_id)
async def region_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    region_id = callback_query.data.split('reg_')[1]
    # ic('new region', region_id)
    await state.update_data(region_id=region_id)
    await callback_query.answer()
    await callback_query.message.answer(saved_message, parse_mode="HTML", reply_markup=update_education_info)
    await UpdateEducation.new_district_id.set()
    
    data = await state.get_data()
    token = data['token']  # Use direct indexing for required data
    region_id = data['region_id']
    district_id_response = send_req.districts(token, int(region_id))  # Ensure it's awaited
    districts = district_id_response.json()  # Async call should be awaited
    # pprint(districts)
    buttons = [[InlineKeyboardButton(text=item['name_uz'], callback_data=f"dist_{item['id']}")] for item in districts]
    districtsMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.answer("Tumanni tanlang:", reply_markup=districtsMenu)
    

@dp.callback_query_handler(lambda c: c.data.startswith('dist_'), state=UpdateEducation.new_district_id)
async def district_selection_handler_new(callback_query: types.CallbackQuery, state: FSMContext):
    new_district_id = callback_query.data.split('dist_')[1]
    data = await state.get_data()
    new_region = data['region_id']
    # ic('new district id', new_district_id)
    token = data.get('token')
    # ic(258, token)

    data_me = await send_req.application_forms_me(token)

    user_education = data_me.get('user_education', {})
    if user_education:
        education_id = user_education.get('education_id', None)
        # district_id =  user_education.get('district_id', None)
        # region_id = user_education.get('region_id', None)
        institution_name = user_education.get('institution_name', None)
        src = user_education.get('src', None)
        file_diploma = user_education.get('file', None)
        await state.update_data(education_id=education_id, district_id=new_district_id, region_id=int(new_region), institution_name=institution_name, src=src, file_diploma=file_diploma[0])
    
    new_data = await state.get_data()
    district_id_= new_data.get('district_id')
    education_id_ = new_data.get('education_id')
    region_id_ = new_data.get('region_id')
    institution_name_ = new_data.get('institution_name')
    src_ = new_data.get('src')
    file_diploma_ = new_data.get('file_diploma')
    # ic(file_diploma)
    # obj = {
    #     int(district_id_),
    #     int(education_id_),
    #     file_diploma_,
    #     institution_name_,
    #     int(region_id_),
    #     src_
    # }
    # ic(obj)
    update_education = send_req.application_forms_for_edu(token,int(district_id_),
                                                                int(education_id_),
                                                                file_diploma_,
                                                                institution_name_,
                                                                int(region_id_),
                                                                src_)
    ic(update_education)
    await state.update_data(district_id=new_district_id)
    await callback_query.answer()
    await callback_query.message.answer(saved_message, parse_mode="HTML", reply_markup=update_education_info)



@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'district', state=UpdateEducation.education_id)
async def update_district(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    token = data['token']  
    region_id = data['region_id']
    district_id_response = send_req.districts(token, int(region_id))  # Ensure it's awaited
    districts = district_id_response.json()  # Async call should be awaited
    # pprint(districts)
    buttons = [[InlineKeyboardButton(text=item['name_uz'], callback_data=f"dist_{item['id']}")] for item in districts]
    districtsMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.answer("Tumanni tanlang:", reply_markup=districtsMenu)

@dp.callback_query_handler(lambda c: c.data.startswith('dist_'), state=UpdateEducation.education_id)
async def district_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    district_id_new = callback_query.data.split('dist_')[1]
    ic(district_id_new)
    data = await state.get_data()
    token = data.get('token')
    # ic(258, token)

    data_me = await send_req.application_forms_me(token)

    user_education = data_me.get('user_education', {})
    if user_education:
        education_id = user_education.get('education_id', None)
        # district_id =  user_education.get('district_id', None)
        region_id = user_education.get('region_id', None)
        institution_name = user_education.get('institution_name', None)
        src = user_education.get('src', None)
        file_diploma = user_education.get('file', None)
        await state.update_data(education_id=education_id, district_id=district_id_new, region_id=int(region_id), institution_name=institution_name, src=src, file_diploma=file_diploma[0])
    
    new_data = await state.get_data()
    district_id_= new_data.get('district_id')
    education_id_ = new_data.get('education_id')
    region_id_ = new_data.get('region_id')
    institution_name_ = new_data.get('institution_name')
    src_ = new_data.get('src')
    file_diploma_ = new_data.get('file_diploma')
    ic(file_diploma)
    obj = {
        int(district_id_),
        int(education_id_),
        file_diploma_,
        institution_name_,
        int(region_id_),
        src_
    }
    ic(obj)
    update_education = send_req.application_forms_for_edu(token,int(district_id_),
                                                                int(education_id_),
                                                                file_diploma_,
                                                                institution_name_,
                                                                int(region_id_),
                                                                src_)
    await state.update_data(district_id=district_id_)
    await callback_query.answer()
    await callback_query.message.answer(saved_message, parse_mode="HTML", reply_markup=update_education_info)

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'education_name', state=UpdateEducation.education_id)
async def update_education_name(callback_query: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN 
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    ic(type_your_edu_name)
    await callback_query.message.answer(type_your_edu_name)
    await UpdateEducation.institution_name.set()


@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'diploma', state=UpdateEducation.education_id)
async def update_diploma(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(example_diploma_message)
    await UpdateEducation.file_diploma.set()

@dp.message_handler(content_types=['document'], state=UpdateEducation.file_diploma)
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
    await message.answer(wait_file_is_loading, parse_mode='HTML')
    # ic(local_file_path)

    res_file = upload.upload_new_file(token=token_, filename=local_file_path)
    # if file_size != 'File not found':
    try:
        file_size = os.path.getsize(local_file_path)
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024
        # print(f'size: {file_size_mb:.2f}')
    except: 
        return 'File not found'
    await state.update_data(file_size=file_size)
    await message.answer("Fayl yuklandi.")
    
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

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'certificate', state=UpdateEducation.education_id)
async def update_diploma(callback_query: types.CallbackQuery, state: FSMContext):

    cert_types = [
        {'id': 1, 'type': 'IELTS'},
        {'id': 2, 'type': 'TOEFL'},
        {'id': 3, 'type': 'CEFR'},
        {'id': 4, 'type': 'SAT'},
        {'id': 5, 'type': 'GMAT'},
        {'id': 6, 'type': 'GRE'},
        {'id': 7, 'type': 'Boshqa'}
    ] 
    buttons = [[InlineKeyboardButton(text=item['type'], 
                                    callback_data=f"type_{item['id']}") for item in cert_types]]
    certTypeMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.answer(select_type_certificate, reply_markup=certTypeMenu)
    await UpdateEducation.certificate_type.set()

# @dp.message_handler(state=UpdateEducation.certificate)
# async def update_certificate(message: types.Message, state: FSMContext):

@dp.callback_query_handler(lambda c: c.data.startswith('type_'), state=UpdateEducation.certificate_type)
async def region_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    certificate_type = callback_query.data.split('type_')[1]
    cert_types = [
            {'id': 1, 'type': 'IELTS'},
            {'id': 2, 'type': 'TOEFL'},
            {'id': 3, 'type': 'CEFR'},
            {'id': 4, 'type': 'SAT'},
            {'id': 5, 'type': 'GMAT'},
            {'id': 6, 'type': 'GRE'},
            {'id': 7, 'type': 'Boshqa'}
        ] 
    cert_types = [item['type'] for item in cert_types if item['id'] == int(certificate_type)]
    ic(cert_types)
    if certificate_type and len(cert_types) > 0:
        certificate_type = str(cert_types[0]).lower()
        ic(certificate_type)
    await state.update_data(certificate_type=certificate_type)
    await callback_query.answer()
    await UpdateEducation.get_certificate.set()  # Proceed to the next state
    # await message.answer(c)
    await callback_query.message.answer(saved_message, parse_mode="HTML")
    await callback_query.message.answer(example_certification_message, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(content_types=['document'], state=UpdateEducation.get_certificate)
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
    await message.answer(wait_file_is_loading, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    # ic(local_file_path)

    res_file = upload.upload_new_file_sertificate(token=token_, filename=local_file_path)
    ic(731, res_file)
    try:
        file_size = os.path.getsize(local_file_path)
        file_size_kb = file_size / 1024
        file_size_mb = file_size_kb / 1024
        ic(f'size: {file_size_mb:.2f}')
    except:
        return 'File not found'
    await state.update_data(file_size_sertificate=file_size)
    # await message.answer("Fayl yuklandi.", reply_markup=ReplyKeyboardRemove())
    # await EducationData.has_application.set()
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
        await message.answer(f"Xatolik: {e}")
        return

    await message.answer("Fayl yuklandi.")
    ic('boshlandi1')
    await message.answer(saved_message, parse_mode="HTML", reply_markup=update_education_info)
    

@dp.message_handler(state=UpdateEducation.institution_name)
async def update_institution_name(message: types.Message, state: FSMContext):
    institution_name_inputed = message.text
    if institution_name_inputed in ["📚 Ta'lim ma'lumotlarni ko'rish", "📝 Ta'lim ma'lumotlarni tahrirlash"]:
        await UpdateEducation.education_id.set()  # Move to the next state or modify as needed
        return 
    data = await state.get_data()
    token = data.get('token')
    # ic(258, token)

    data_me = await send_req.application_forms_me(token)

    user_education = data_me.get('user_education', {})
    if user_education:
        education_id = user_education.get('education_id')
        district_id = user_education.get('district_id')
        region_id = user_education.get('region_id')
        src = user_education.get('src')
        file_diploma = user_education.get('file', [None])[0]  # Safely get the first item or None

        await state.update_data(
            education_id=education_id,
            district_id=district_id,
            region_id=int(region_id) if region_id is not None else None,
            institution_name=institution_name_inputed,
            src=src,
            file_diploma=file_diploma
        )

        # Log or process updated data
        ic({
            "district_id": district_id,
            "education_id": education_id,
            "region_id": region_id,
            "institution_name": institution_name_inputed,
            "src": src,
            "file_diploma": file_diploma
        })

        # Send the update to the server (assuming synchronous call, add await if async)
        update_education = send_req.application_forms_for_edu(
            token,
            int(district_id),
            int(education_id),
            file_diploma,
            institution_name_inputed,
            int(region_id),
            src
        )
        ic(update_education)
        await state.update_data(institution_name=institution_name_inputed)
        await message.answer(saved_message, parse_mode="HTML", reply_markup=update_education_info)

    await UpdateEducation.next()

@dp.message_handler(Text(equals="📚 Ta'lim ma'lumotlarni ko'rish"), state="*")
async def education_menu(message: Message, state: FSMContext):

    data = await state.get_data()
    ic('keldi700', data)
    token = data.get('token')
    haveApplicationForm = data.get('haveApplicationForm')
    haveApplied = data.get('haveApplied')
    # haveEducation = data.get('haveEducation')
    # havePreviousEducation = data.get('havePreviousEducation')
    register_user = data.get('register_user')
    transfer_user = data.get('transfer_user')
    education_info = await send_req.application_forms_me(token)
    ic(education_info)
    haveEducation = education_info.get('haveEducation')
    havePreviousEducation = education_info.get('havePreviousEducation')
    ic('shu keldi:', haveEducation)
    if token and haveEducation:
        education_info = await send_req.application_forms_me(token)
        ic(education_info)
        user_education = education_info.get('user_education', {})
        certifications = education_info.get('certifications', [])
        # if certifications:
        #     if len(certifications) >= 2:
        #         certifications = certifications[-1]
            
        pinfl_user_education = education_info.get('pinfl_user_education', {})
        # ic(education_info)
        # ic(certifications)
        # ic(pinfl_user_education)
        # ic(user_education)
        # Constructing the education message
        education_message = "<b>📚 Ta'lim Ma'lumotlari:</b>\n\n"
        if user_education.get('education_type_uz', None) is not None:
            education_message += (
                f"• <b>Ta'lim turi:</b> {user_education.get('education_type_uz', 'Talim turi topilmadi')}\n"
                f"• <b>Viloyat:</b> {user_education.get('region_name_uz', 'Viloyat topilmadi')}\n"
                f"• <b>Tuman:</b> {user_education.get('district_name_uz', 'Tuman topilmadi')}\n"
                f"• <b>O'quv muassasasi nomi:</b> {user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
            )
        elif pinfl_user_education['institution_name'] is not None:
            institution_type = pinfl_user_education.get('institution_type', 'Talim turi topilmadi')
            if institution_type == 'school':
                institution_type = 'Maktab'
            education_message += (
                # f"• <b>Daraja:</b> {pinfl_user_education.get('degree_name_uz', 'Daraja topilmadi')}\n"
                # f"• <b>Tamomlagan yil:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Tamomlagan yil topilmadi')}\n"
                # f"• <b> Mamlakat:</b> {pinfl_user_education.get('country', 'Shahar topilmadi')}\n"
                f"• <b>Shahar:</b> {pinfl_user_education.get('region', 'Shahar nomi topilmadi')}\n"
                f"• <b>Tuman:</b> {pinfl_user_education.get('district', 'Tuman nomi topilmadi')}\n"
                f"• <b>Ta'lim turi:</b> {institution_type}\n"
                f"• <b>O'quv muassasasi nomi:</b> {pinfl_user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
            )

        # Sending the educational info message
        await message.answer(education_message, parse_mode="HTML", reply_markup=menu)

        diploma_file = user_education.get('file')
        if diploma_file is not None:
            try:
                await message.answer_document(f"https://{domain_name}/{diploma_file[0]}", caption="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli")
            except Exception as e:
                print(f"Failed to send diploma file: {e}")
        elif pinfl_user_education:
            try:
                await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli")
            except Exception as e:
                print(f"Failed to send diploma file: {e}")
            
        # Sending certification files if available

        ic(124)
        ic(certifications)
        for certification in certifications:
            if certification.get('file'):
                ic(127)
                certification_type = certification.get('certification_type', 'Sertifikat turi topilmadi')
                try:
                    await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Sertifikat nusxasi: {certification_type.upper()}")
                except Exception as e:
                    print(f"Failed to send certification file: {e}")   
    elif havePreviousEducation:
        ic('mytoken', token)
        education_info = await send_req.application_forms_me(token)
        ic(education_info)
        user_education = education_info.get('user_previous_education', None)
        pinfl_user_education = education_info.get('pinfl_user_education', {})

        certifications = education_info.get('certifications', [])
        if user_education is not None:
            education_message = "<b>📚 Ta'lim Ma'lumotlari:</b>\n\n"
            education_message += (
                f"• <b>Mamlakat:</b> {user_education.get('country_name_uz', 'Viloyat topilmadi')}\n"
                f"• <b>O'quv muassasasi nomi:</b> {user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
                f"""• <b>Yo'nalish:</b> {user_education.get('direction_name', "Yonalish topilmadi")}\n"""
                f"• <b>Kurs:</b> {user_education.get('which_course_now', 'Daraja topilmadi')}-chi kurs\n"
            )
            
            if pinfl_user_education is not None:
                if pinfl_user_education['pinfl_region_id'] is not None:
                    education_message += (
                        f"• <b>Daraja:</b> {pinfl_user_education.get('degree_name_uz', 'Daraja topilmadi')}\n"
                        f"• <b>Tamomlagan yil:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Tamomlagan yil topilmadi')}\n"
                        f"• <b> Mamlakat:</b> {pinfl_user_education.get('country', 'Shahar topilmadi')}\n"
                        f"• <b>Shahar:</b> {pinfl_user_education.get('region', 'Shahar nomi topilmadi')}\n"
                        f"• <b>Tuman:</b> {pinfl_user_education.get('district', 'Tuman nomi topilmadi')}\n"
                        f"• <b>Ta'lim turi:</b> {pinfl_user_education.get('institution_type', 'Talim turi topilmadi')}\n"
                        f"• <b>O'quv muassasasi nomi:</b> {pinfl_user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
                )
            await message.answer(education_message, parse_mode="HTML", reply_markup=menu)

            transcript_file = user_education.get('transcript_file')
            if transcript_file:
                try:
                    await message.answer_document(f"https://{domain_name}/{transcript_file}", caption="Transkript nusxasi fayli")
                except Exception as e:
                    print(f"Failed to send diploma file: {e}")
            elif pinfl_user_education:
                try:
                    await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi fayli")
                except Exception as e:
                    print(f"Failed to send diploma file: {e}")
                
            # Sending certification files if available

            ic(124)
            if certifications is not None and certifications:
                for certification in certifications:
                    if certification.get('file'):
                        ic(127)
                        certification_type = certification.get('certification_type', 'Sertifikat turi topilmadi')
                        try:
                            await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Sertifikat nusxasi: {certification_type.upper()}")
                        except Exception as e:
                            print(f"Failed to send certification file: {e}") 
    else:

        await message.answer("Kechirasiz, sizning ma'lumotlaringizni olish imkoni bo'lmadi. Iltimos, akkauntdan chiqib tizimga qayta kiring.", reply_markup=menu)
        # await message.answer("Kechirasiz, sizning ma'lumotlaringizni olish imkoni bo'lmadi. Iltimos,akkuntdan chiqib tizimga qayta kiring.", reply_markup=menu)


#TODO arizam
@dp.message_handler(Text(equals=["📁Arizam","📁arizam"]), state=PersonalData.country_search)
async def my_application(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    ic('keldi arizaga')
    my_app = await send_req.my_applications(token=token)
    if not my_app:
        await message.answer("Ariza ma'lumotlari topilmadi.")
        return

    created_at = my_app.get('created_at', 'yaratilgan vaqti topilmadi')
    status = my_app.get('status', 'status topilmadi')
    comments = my_app.get('comment', 'izoh topilmadi')
    # status1 = my_app.get('status')
    # ic(status1)
    direction_name_uz = my_app.get('direction_name_uz', 'Talim turi topilmadi')
    degree_name_uz = my_app.get('degree_name_uz', 'Talim darajasi topilmadi')
    education_type_name_uz = my_app.get('education_type_name_uz','Talim turi topilmadi' )
    education_language_name_uz = my_app.get('education_language_name_uz', 'Talim tili topilmadi')
    tuition_fee = my_app.get('tuition_fee', 'Narxi topilmadi')
    date_obj = datetime.fromisoformat(created_at.rstrip("Z"))
    utc_timezone = pytz.timezone('UTC')
    desired_timezone = pytz.timezone('Asia/Tashkent')  # Replace 'Asia/Tashkent' with your desired timezone
    date_obj = utc_timezone.localize(date_obj).astimezone(desired_timezone)
    human_readable_date = date_obj.strftime("%Y-%m-%d %H:%M")
    if len(comments) >= 2:
        comments = comments[-1]
    if tuition_fee != 'Narxi topilmadi':
        formatted_fee = "{:,.0f}".format(tuition_fee).replace(',', '.')

    applicant_status_translations = {
    'PENDING': 'kutilmoqda',
    'ACCEPTED': 'qabul qilingan',
    'REJECTED': 'rad etilgan',
    'EDIT-REJECT': 'tahrirlash uchun ariza rad etildi',
    'CALLED-EXAM': 'imtihonga chaqirilgan',
    'EXAM-FEE': 'imtihon uchun to\'lov to\'langan',
    'CAME-EXAM': 'imtihonga kelgan',
    'MARKED': 'baholangan',
    'SUCCESS': 'muvaffaqiyatli',
    'FAIL': 'muvaqqiyatsiz',
    'CONTRACT': 'shartnoma',
    'STUDENT': 'talaba',
    'RECOMMENDED_STUDENT': 'tavsiya etilgan talaba'
    }
    comment = comments.get('comment', 'izoh topilmadi')
    comment_time = comments.get('created_at', 'izoh vaqti topilmadi')
    if comment_time != 'izoh vaqti topilmadi':
        comment_time = convert_time(comment_time)
    status_name = applicant_status_translations.get(status.upper(), "Topilmadi")
    response_message = (
        f"<b>Ariza Tafsilotlari:</b>\n"
        f"Yaratilgan vaqti: {human_readable_date}\n"
        f"Holati:   <b>{status_name}</b>\n"
        f"Yo'nalishi: {direction_name_uz}\n"
        f"Darajasi: {degree_name_uz}\n"
        f"Ta'lim turi: {education_type_name_uz}\n"
        f"Ta'lim til: {education_language_name_uz}\n"
        f"Ta'lim narix: {formatted_fee} so'm\n"
        f"Izoh vaqti {escape_markdown(comment_time)}"
        f" 🔴 Izoh: {escape_markdown(comment)}\n"
    )
    await message.answer(response_message, parse_mode='HTML')


@dp.message_handler(Text(equals="📁Arizam"), state="*")
async def my_application(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    ic('keldi arizaga')
    my_app = await send_req.my_applications(token=token)
    ic(my_app)
    if not my_app:
        await message.answer("Ariza ma'lumotlari topilmadi.")
        return

    created_at = my_app.get('created_at', 'yaratilgan vaqti topilmadi')
    status = my_app.get('status', 'status topilmadi')
    direction_name_uz = my_app.get('direction_name_uz', 'Talim turi topilmadi')
    degree_name_uz = my_app.get('degree_name_uz', 'Talim darajasi topilmadi')
    education_type_name_uz = my_app.get('education_type_name_uz','Talim turi topilmadi' )
    education_language_name_uz = my_app.get('education_language_name_uz', 'Talim tili topilmadi')
    tuition_fee = my_app.get('tuition_fee', 'Narxi topilmadi')
    comments = my_app.get('comment', [])
    date_obj = datetime.fromisoformat(created_at.rstrip("Z"))
    utc_timezone = pytz.timezone('UTC')
    desired_timezone = pytz.timezone('Asia/Tashkent')  # Replace 'Asia/Tashkent' with your desired timezone
    date_obj = utc_timezone.localize(date_obj).astimezone(desired_timezone)
    human_readable_date = date_obj.strftime("%Y-%m-%d %H:%M")
    if len(comments) >= 2:
        comments = comments[-1]
    if tuition_fee != 'Narxi topilmadi':
        formatted_fee = "{:,.0f}".format(tuition_fee).replace(',', '.')

    applicant_status_translations = {
    'PENDING': 'kutilmoqda',
    'ACCEPTED': 'qabul qilingan',
    'REJECTED': 'rad etilgan',
    'EDIT-REJECT': 'tahrirlash uchun ariza rad etildi',
    'CALLED-EXAM': 'imtihonga chaqirilgan',
    'EXAM-FEE': 'imtihon uchun to\'lov to\'langan',
    'CAME-EXAM': 'imtihonga kelgan',
    'MARKED': 'baholangan',
    'SUCCESS': 'muvaffaqiyatli',
    'FAIL': 'muvaqqiyatsiz',
    'CONTRACT': 'shartnoma',
    'STUDENT': 'talaba',
    'RECOMMENDED_STUDENT': 'tavsiya etilgan talaba'
    }
    ic(comments)
    if comments:
        try:
            comment = comments['comment']
            comment_time = convert_time(comments['created_at'])
        except:
            comment = comments[0]['comment']
            comment_time = convert_time(comments[0]['created_at'])
    else:
        comment = 'izoh topilmadi'
        comment_time = 'izoh vaqti topilmadi'
    status_name = applicant_status_translations.get(status.upper(), "Topilmadi")

    
    response_message = (
        f"*Ariza Tafsilotlari:*\n"
        f"Yaratilgan vaqti: {escape_markdown(human_readable_date)}\n"
        f"Holati:   *{escape_markdown(status_name)}*\n"
        f"Yo'nalishi: {escape_markdown(direction_name_uz)}\n"
        f"Darajasi: {escape_markdown(degree_name_uz)}\n"
        f"Ta'lim turi: {escape_markdown(education_type_name_uz)}\n"
        f"Ta'lim til: {escape_markdown(education_language_name_uz)}\n"
        f"Ta'lim narxi: {escape_markdown(formatted_fee)} so'm\n\n"
        f"Izoh vaqti: {escape_markdown(comment_time)}\n"
        f"🔴 *Izoh:* {escape_markdown(comment)}\n"
    )
    await message.answer(response_message, parse_mode='MarkdownV2')