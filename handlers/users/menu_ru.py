from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.default.registerKeyBoardButton import menu_ru, application_ru, ask_delete_account_ru,exit_from_account_ru, update_personal_info_ru,finish_edit_ru,update_education_info_ru
from keyboards.inline.menukeyboards import update_personal_info_inline_ru,edit_user_education_inline_ru,edit_user_education_transfer_inline_ru
from states.personalData import PersonalDataRU, UpdateMenuRU,UpdateEducationRU,EducationDataRU
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
from data.config import university_id as UNIVERSITY_ID
from handlers.users import upload,collect_data
from handlers.users.register_ru import saved_message_ru,select_region_ru,type_your_edu_name_ru,example_diploma_message_ru,wait_file_is_loading_ru,select_type_certificate_ru,example_certification_message_ru,not_found_country_ru,search_university_ru,select_one_ru
start_button = KeyboardButton('/start')  # The text on the button
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)
escape_markdown = send_req.escape_markdown
convert_time = send_req.convert_time
@dp.message_handler(Text(equals="🗑 Удаление аккаунта"), state="*")
async def delete_account_prompt(message: types.Message, state: FSMContext):
    await message.answer("Удалить аккаунт?", reply_markup=ask_delete_account_ru)

@dp.message_handler(Text(equals="Да, удалить аккаунт"), state="*")
async def delete_account(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    delete_account_result = await send_req.delete_profile(token)
    ic(delete_account_result)
    if delete_account_result == 200:
        await state.update_data(start_count=0)
        response_message = "Ваша учетная запись успешно удалена."
    else:
        response_message = f"Произошла ошибка: {delete_account_result.get('error')}"
    await state.update_data(token=None)
    await message.answer(response_message, reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(state=EducationDataRU.menu)
# async def show_menu(message: Message):
#     await message.answer("Akkauntga hush kelibsiz!", reply_markup=menu)


@dp.message_handler(Text(equals="Выйти из аккаунта"), state="*")
async def ask_exit_menu(message: Message, state: FSMContext):
    await message.answer("Вы хотите выйти из системы?", reply_markup=exit_from_account_ru)

@dp.message_handler(Text(equals="Да, выйти"), state="*")
async def exit_menu(message: Message, state: FSMContext):
    await state.update_data(token=None)
    await state.update_data(start_count=0)
    await message.answer('Вы вышли из системы.\nНажмите «Начать», чтобы войти снова.', reply_markup=start_keyboard)

@dp.message_handler(Text(equals="Отмена"), state="*")
async def stay_menu(message: Message, state: FSMContext):
    await message.answer("Главная страница", reply_markup=menu_ru)

@dp.message_handler(Text(equals="ℹ️Моя личная информация"), state="*")
async def my_menu(message: Message, state: FSMContext):
    ic('Quyidagi amallarni bajarishingiz mumkin')
    await message.answer("Вы можете выполнить следующие шаги", reply_markup=update_personal_info_ru)


@dp.message_handler(Text(equals="📄Просмотр личной информации"), state="*")
async def my_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    ic(66)
    token = data.get('token')
    ic(token)
    ic(74)
    if token:
        ic('token mavjud, shaxsiy ma\'lumotlarni ko\'rish', token)
        personal_info = await send_req.application_forms_me(token)
        
        photo = f"https://{domain_name}/{personal_info['photo']}" if f"https://{domain_name}/{personal_info['photo']}" else 'Изображение не найдено'
        ic(photo)
        
        first_name = personal_info['first_name'] if personal_info['first_name'] else 'имя не найдено'
        last_name = personal_info['last_name'] if personal_info['last_name'] else 'фамилия не найдена'
        third_name = personal_info['third_name'] if personal_info['third_name'] else 'имя отца не найдено'
        serial_number = personal_info['serial_number'] if personal_info['serial_number'] else 'серийный номер и номер не найдены'
        birth_date = send_req.convert_time(personal_info['birth_date'])  if send_req.convert_time(personal_info['birth_date']) else 'дата рождения не найдена'
        pin = personal_info['pin'] if personal_info['pin'] else "JSHSHR topilmadi"
        gender = 'erkak' if personal_info.get('gender') == 'male' else 'ayol' if personal_info.get('gender') == 'female' else 'jins topilmadi'

        citizenship = personal_info['citizenship'] if personal_info['citizenship'] else "Республика Узбекистан"
        birth_place = personal_info['birth_place'] if personal_info['birth_place'] else 'место рождения не найдено'
        phone = personal_info['phone'] if personal_info['phone'] else 'номер телефона не найден'
        extra_phone = personal_info['extra_phone'].replace(" ", "") if personal_info['extra_phone'] else 'дополнительный номер телефона не найден'
        info_message = (
        "<b>Персональная информация:</b>\n\n"
        f"• <b>Имя:</b> {first_name}\n"
        f"• <b>Фамилия:</b> {last_name}\n"
        f"• <b>Имя Отца:</b> {third_name}\n"
        f"• <b>Серия и номер:</b> {serial_number}\n"
        f"• <b>Дата рождения:</b> {birth_date}\n"
        f"• <b>ПИНФЛ:</b> {pin}\n"
        f"• <b>Пол:</b> {gender}\n"
        f"• <b>Гражданство:</b> {citizenship}\n"
        f"• <b>Место рождения:</b> {birth_place}\n"
        f"• <b>Номер телефона:</b> {phone}\n"
        f"• <b>Дополнительный номер телефона:</b> {extra_phone.strip()}\n"
        )
        await message.answer_photo(photo, caption=info_message, reply_markup=menu_ru, parse_mode="HTML")
    else:
        await message.answer('Информация профиля не найдена\nНажмите «Начать», чтобы войти снова.', reply_markup=start_keyboard)

@dp.message_handler(Text(equals="📝 Редактировать личную информацию"), state="*")
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
                                                        pin=1,date=date, username=username,
                                                        university_name=int(UNIVERSITY_ID))
    ic(save_chat_id)

    get_this_user = send_req.get_user_profile(chat_id=user_chat_id, university_id=UNIVERSITY_ID)
    ic(get_this_user)
    data = await state.get_data()
    token = data.get('token')
    # update_personal_info_inline_dict = update_personal_info_inline.to_dict()
    # # Convert dictionary to JSON string
    # update_personal_info_inline_json = json.dumps(update_personal_info_inline_dict)
    await message.answer('Какую информацию вы хотите отредактировать?',
                          reply_markup=update_personal_info_inline_ru)
    await UpdateMenuRU.firstname.set()





@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata, state=UpdateMenuRU.firstname)
async def update_personal_info_hand(callback_query: types.CallbackQuery, state: FSMContext):
    my_callback = callback_query.data
    ic(my_callback)
    await state.update_data(callback=my_callback)
    my_obj = {
        'firstname': 'Введите имя, которое хотите обновить: ',
        'lastname': 'Введите фамилию, которую хотите обновить.',
        'thirdname': 'Введите имя отца, которого вы хотите обновить.',
        'passport': 'Введите серийный номер паспорта, который вы хотите обновить, в следующем формате: AB1234567.',
        'birthdate': 'Введите дату рождения, которую вы хотите обновить, в формате Qui: гггг-мм-дд.',
        'gender': 'Введите пол, который вы хотите обновить, в следующем формате: Мужской/Женский.',
        'birthplace': 'Введите место рождения, которое вы хотите обновить. Пример: город Ташкент.',
        'extra_phone': 'Введите дополнительный номер телефона, который вы хотите обновить. Пример: +998991234567.',
    }
    res_mess = my_obj.get(my_callback)
    await callback_query.message.answer(res_mess)
    await UpdateMenuRU.lastname.set()

@dp.message_handler(state=UpdateMenuRU.lastname)
async def get_user_input(message: types.Message, state: FSMContext):
    
    user_input = message.text
    if user_input == "📚 Просмотр образовательной информации" or user_input == "📚Моя образовательная информация":
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
        if user_input == 'Мужской':
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
    await message.answer(saved_message_ru)
    await UpdateMenuRU.firstname.set()


@dp.message_handler(Text(equals="📚Моя образовательная информация"), state="*")
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
                                                            pin=1,date=date, username=username,
                                                            university_name=int(UNIVERSITY_ID))
        ic(save_chat_id)

        get_this_user = send_req.get_user_profile(chat_id=user_chat_id, university_id=UNIVERSITY_ID)
        ic(get_this_user)
    except Exception as err:
        ic(err)

    await message.answer("Выберите один ниже", reply_markup=update_education_info_ru)

@dp.message_handler(Text(equals="📝 Редактировать образовательную информацию"), state="*")
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
            await message.answer("Какую информацию вы хотите отредактировать?",
                                    reply_markup=edit_user_education_inline_ru)
            await UpdateEducationRU.education_id.set()
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
        await PersonalDataRU.country_search.set()
        ic('perevod uchun keldi')
        await message.answer("Какую информацию вы хотите отредактировать?",reply_markup=edit_user_education_transfer_inline_ru)

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'country_id', state=EducationDataRU.country_search)
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
        await PersonalDataRU.country_search.set()  # Assuming country_search is a state for inputting country search
        

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'country_id', state=PersonalDataRU.country_search)
async def education_id_handler(callback_query: types.CallbackQuery, state: FSMContext, page: int = 0):
    ic('shu yer ekan')
    await callback_query.message.answer(search_university_ru, reply_markup=ReplyKeyboardRemove())
    await PersonalDataRU.country_search.set()

@dp.message_handler(lambda message: message.text in ["📚 Просмотр образовательной информации", "📝 Редактировать образовательную информацию"],state=PersonalDataRU.country_search)
async def handle_education_options(message: types.Message, state: FSMContext):
    # Direct handling for specific commands
    # Redirect to appropriate handlers or reset state based on the command
    if message.text == "📚 Просмотр образовательной информации":
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
            education_message = "<b>📚 Образовательная информация:</b>\n\n"
            # Constructing the education message
            if education_info.get('user_education_src', None) == 'automatic':
                # ic(education_info.get('user_education_src', None))
                ic('keldi 348')
                education_message += (
                    f"• <b>Тип образования:</b> {user_education.get('education_type_uz', 'Тип обучения не найден')}\n"
                    f"• <b>Регион:</b> {user_education.get('region_name_uz', 'Регион не найден')}\n"
                    f"• <b>Район:</b> {user_education.get('district_name_uz', 'Район не найден')}\n"
                    f"• <b>Название учебного заведения:</b> {user_education.get('institution_name', 'Название учебного заведения не найдено')}\n"
                )
            elif education_info['user_education_src'] != 'automatic':
                # ic(education_info['user_education_src'])
                ic('keldi 357')
                education_message += (
                    f"• <b>Степень:</b> {pinfl_user_education.get('degree_name_uz', 'Степень не найден')}\n"
                    f"• <b>Выпускной год:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Год окончания не найден')}\n"
                    f"• <b>Страна:</b> {pinfl_user_education.get('country', 'Страна не найдена')}\n"
                    f"• <b>Города:</b> {pinfl_user_education.get('region', 'Название города не найдено')}\n"
                    f"• <b>Туман:</b> {pinfl_user_education.get('district', 'Название района не найдено')}\n"
                    f"• <b>Тип образования:</b> {pinfl_user_education.get('institution_type', 'Тип обучения не найден')}\n"
                    f"• <b>Название учебного заведения:</b> {pinfl_user_education.get('institution_name', 'Название учебного заведения не найдено')}\n"
                    f"• <b>Номер диплома или сертификата:</b> {pinfl_user_education.get('document', 'Номер диплома или сертификата не найдено')}\n"
                )

            # Sending the educational info message
            await message.answer(education_message, parse_mode="HTML", reply_markup=menu_ru)

            diploma_file = user_education.get('file')
            if diploma_file is not None:
                try:
                    await message.answer_document(f"https://{domain_name}/{diploma_file[0]}", caption="Копия диплома, сертификата или справочного файла.")
                except Exception as e:
                    print(f"Не удалось отправить файл диплома.: {e}")
                    await message.answer(chat_id=message.chat.id, text="Файл копии диплома, сертификата или справки не найден. Перезагрузите.")

            elif pinfl_user_education['file'][0] is not None:
                try:
                    await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Копия диплома, сертификата или справочного файла.")
                except Exception as e:
                    print(f"Не удалось отправить файл диплома.: {e}")
                    await message.answer(chat_id=message.chat.id, text="Файл копии диплома, сертификата или справки не найден. Перезагрузите.")

                
            # Sending certification files if available

            ic(398)
            if certifications:
                for certification in certifications:
                    if certification.get('file'):
                        ic(127)
                        certification_type = certification.get('certification_type', 'Тип сертификата не найден')
                        try:
                            await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Копия сертификата: {certification_type.upper()}")
                        except Exception as e:
                            print(f"Не удалось отправить файл сертификации.: {e}")   
                            await message.answer(chat_id=message.chat.id, text=f"Копия сертификата: {certification_type.upper()} не найдено, перезагрузить")
        elif token and havePreviousEducation:
            ic('mytoken', token)
            education_info = await send_req.application_forms_me(token)
            ic(education_info)
            user_education = education_info.get('user_previous_education', None)
            pinfl_user_education = education_info.get('pinfl_user_education', {})

            certifications = education_info.get('certifications', [])
            if user_education is not None:
                education_message = "<b>📚 Образовательная информация:</b>\n\n"
                education_message += (
                    f"• <b>Страна:</b> {user_education.get('country_name_uz', 'Страна не найдено')}\n"
                    f"• <b>Название учебного заведения:</b> {user_education.get('institution_name', 'Название института не найдено')}\n"
                    f"""• <b>Название направления:</b> {user_education.get('direction_name', "Направления не найден")}\n"""
                    f"• <b>Курс:</b> {user_education.get('which_course_now', 'Степень не найден')}- степень\n"
                )
                
                if pinfl_user_education is not None:
                    if pinfl_user_education['pinfl_region_id'] is not None:
                        education_message += (
                            f"• <b>Степень:</b> {pinfl_user_education.get('degree_name_uz', 'Степень не найден')}\n"
                            f"• <b>Выпускной год:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Tamomlagan yil topilmadi')}\n"
                            f"• <b> Страна:</b> {pinfl_user_education.get('country', 'Страна не найдена')}\n"
                            f"• <b>Город:</b> {pinfl_user_education.get('region', 'Город не найден')}\n"
                            f"• <b>Район:</b> {pinfl_user_education.get('district', 'Район не найден')}\n"
                            f"• <b>Тип образования:</b> {pinfl_user_education.get('institution_type', 'Тип образования не найдена')}\n"
                            f"• <b>Название учебного заведения:</b> {pinfl_user_education.get('institution_name', 'Название учебного заведения не найдена')}\n"
                    )
                await message.answer(education_message, parse_mode="HTML", reply_markup=menu_ru)

                transcript_file = user_education.get('transcript_file')
                if transcript_file:
                    try:
                        await message.answer_document(f"https://{domain_name}/{transcript_file}", caption="Копия файла транскрипта")
                    except Exception as e:
                        print(f"Не удалось отправить файл диплома.: {e}")
                        await message.answer(chat_id=message.chat.id, text="Файл копии транскрипта не найден. Перезагрузите.")
                elif pinfl_user_education:
                    try:
                        await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Копия диплома, сертификата или справочного файла.")
                    except Exception as e:
                        print(f"Не удалось отправить файл диплома.: {e}")
                        await message.answer(chat_id=message.chat.id, text="Файл копии диплома, сертификата или справки не найден. Перезагрузите.")
                    
                # Sending certification files if available

                ic(124)
                if certifications is not None and certifications:
                    for certification in certifications:
                        if certification.get('file'):
                            ic(127)
                            certification_type = certification.get('certification_type', 'Тип сертификата не найден')
                            try:
                                await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Копия сертификата: {certification_type.upper()}")
                            except Exception as e:
                                print(f"Не удалось отправить файл сертификации.: {e}") 
                                await message.answer(chat_id=message.chat.id, text="Файл копии сертификата не найден. Перезагрузите.")
        else:

            # Handle the case where the token is None or invalid
            await message.answer("К сожалению, вашу информацию не удалось получить. Пожалуйста, выйдите из системы и войдите снова.")
        # Example: Navigate to viewing educational data
        # await message.answer("📚 Ta'lim ma'lumotlari", reply_markup=update_education_info)
    # elif message.text == "📝 Ta'lim ma'lumotlarni tahrirlash":
    #     # Example: Navigate to editing educational data
    #     await message.answer("📝 Ta'lim ma'lumotlarni tahrirlash", reply_markup=)
    # await state.reset_state() 

@dp.message_handler(Text(equals=["📁Заявление","📁заявление"]), state=PersonalDataRU.country_search)
async def my_application(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    ic('keldi arizaga')
    my_app = await send_req.my_applications(token=token)
    ic(my_app)
    if not my_app:
        await message.answer("Информация о заявление не найдена.")
        return

    created_at = my_app.get('created_at', 'время создания не найдено')
    status = my_app.get('status', 'статус не найден')
    direction_name_uz = my_app.get('direction_name_uz', 'Тип обучения не найден')
    degree_name_uz = my_app.get('degree_name_uz', 'Уровень образования не найден')
    education_type_name_uz = my_app.get('education_type_name_uz','Тип обучения не найден' )
    education_language_name_uz = my_app.get('education_language_name_uz', 'Язык обучения не найден')
    tuition_fee = my_app.get('tuition_fee', 'Цена не найдена')
    comments = my_app.get('comment', 'Комментарий не найден')
    date_obj = datetime.fromisoformat(created_at.rstrip("Z"))
    utc_timezone = pytz.timezone('UTC')
    desired_timezone = pytz.timezone('Asia/Tashkent')  # Replace 'Asia/Tashkent' with your desired timezone
    date_obj = utc_timezone.localize(date_obj).astimezone(desired_timezone)
    human_readable_date = date_obj.strftime("%Y-%m-%d %H:%M")
    if len(comments) >= 2:
        comments = comments[-1]
    
    if tuition_fee != 'Цена не найдена':
        formatted_fee = "{:,.0f}".format(tuition_fee).replace(',', '.')
    ic(status)
    applicant_status_translations = {
    'PENDING': 'ожидается',
    'ACCEPTED': 'принято',
    'REJECTED': 'отклоненный',
    'EDIT-REJECT': 'Запрос на редактирование отклонен',
    'CALLED-EXAM': 'вызвали на экзамен',
    'EXAM-FEE': 'плата за экзамен оплачена',
    'CAME-EXAM': 'пришел на экзамен',
    'MARKED': 'оценивается',
    'SUCCESS': 'успешный',
    'FAIL': 'не успешный',
    'CONTRACT': 'договор',
    'STUDENT': 'студент',
    'RECOMMENDED_STUDENT': 'рекомендуемый студент'
    }
    status_name = applicant_status_translations.get(status.upper(), "Не найдено")
    comment = comments.get('comment', 'Комментарий не найден')
    comment_time = comments.get('created_at', 'Комментарий не найден')
    if comment_time != 'Комментарий не найден':
        comment_time = datetime.fromisoformat(comment_time.rstrip("Z")).strftime("%Y-%m-%d %H:%M")
    ic(my_app.get('status'))
    color = 'blue' if comment == 'Комментарий не найден' else 'red'
    if color == 'blue':
        color = "🔵"
    elif color == 'red':
        color = "🔴"    
    response_message = (
        f"<b>Детали Заявлений:</b>\n"
        f"Время создания: {human_readable_date}\n"
        f"Статус:   <b>{status_name}</b>\n"
        f"Направление: {direction_name_uz}\n"
        f"Степень: {degree_name_uz}\n"
        f"Тип образования: {education_type_name_uz}\n"
        f"Язык обучения: {education_language_name_uz}\n"
        f"Стоимость обучения: {formatted_fee} so'm\n"
        f"Время комментирования: {comment_time}\n"
        f" {color} Объяснение: {comment}"
    )
    await message.answer(response_message, parse_mode='HTML')

@dp.message_handler(state=PersonalDataRU.country_search)
async def process_country_search(message: types.Message, state: FSMContext):
    ic("keldi 268")
    user_query = message.text.lower()
    if user_query in ["📚 Посмотреть образовательную информацию", "📝 Редактировать образовательную информацию","📁Заявление",
                      "📁заявление"]:
        await PersonalDataRU.country_search.set()
        return
    ic('user_query', user_query)
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
    await PersonalDataRU.country_search.set()
    # await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('country_'), state=PersonalDataRU.country_search)
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
    await callback_query.message.answer(saved_message_ru, reply_markup=update_education_info_ru)



@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'institution_name', state=PersonalDataRU.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    
    await call.message.answer("Введите название учебного заведения", reply_markup=update_education_info_ru)
    await PersonalDataRU.transfer_edu_name.set()

@dp.message_handler(state=PersonalDataRU.transfer_edu_name)
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
    await message.answer(saved_message_ru, reply_markup=update_education_info_ru)
    ic(application_forms_transfer)
    await state.update_data(institution_name=inst_name)
    await PersonalDataRU.country_search.set()

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'direction_name', state=PersonalDataRU.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название направления обучения:", reply_markup=update_education_info_ru)
    await PersonalDataRU.transfer_direction_name.set()

@dp.message_handler(state=PersonalDataRU.transfer_direction_name)
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
    await message.answer(saved_message_ru, reply_markup=update_education_info_ru)
    await PersonalDataRU.country_search.set()

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'current_course', state=PersonalDataRU.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите курс, который вы хотите обновить: образец 1 или 2.", reply_markup=update_education_info_ru)
    await PersonalDataRU.current_course.set()

@dp.message_handler(state=PersonalDataRU.current_course)
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
    await message.answer(saved_message_ru, reply_markup=update_education_info_ru)
    await PersonalDataRU.country_search.set()


@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'transcript', state=PersonalDataRU.country_search)
async def update_education_transfer(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отправьте копию транскрипта, которую вы хотите обновить.:", reply_markup=update_education_info_ru)
    await PersonalDataRU.transcript.set()


@dp.message_handler(content_types=['document'], state=PersonalDataRU.transcript)
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
        await message.answer(saved_message_ru, reply_markup=update_education_info_ru)
        await state.update_data(file_diploma_transkript=path)
        
    except Exception as e:
        ic(e)
        await message.answer(e)
        return e
    await PersonalDataRU.country_search.set()


@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'education', state=UpdateEducationRU.education_id)
async def update_education(call: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN  
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    data = await state.get_data()
    token = data.get('token')
    educations_response = send_req.educations(token) 
    educations = educations_response.json()  
    
    buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"edu_{item['id']}")] for item in educations]
    educationMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(call.from_user.id,"<b>Выберите тип учебного заведения, которое вы окончили или учитесь в настоящее время:</b>", parse_mode='HTML',reply_markup=educationMenu)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('edu_'), state=UpdateEducationRU.education_id)
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
    await UpdateEducationRU.region_id.set()
    await bot.send_message(callback_query.from_user.id, saved_message_ru, parse_mode="HTML", reply_markup=update_education_info_ru)

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'region', state=UpdateEducationRU.education_id)
async def update_region(callback_query: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    data = await state.get_data()
    token = data['token']
    region_response = send_req.regions(token)
    regions = region_response.json()
    buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"reg_{item['id']}")] for item in regions]
    regionMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(callback_query.from_user.id,select_region_ru, reply_markup=regionMenu)

@dp.callback_query_handler(lambda c: c.data.startswith('reg_'),state=UpdateEducationRU.education_id)
async def region_selection_handler(callback_query: types.CallbackQuery, state: FSMContext):
    region_id = callback_query.data.split('reg_')[1]
    # ic('new region', region_id)
    await state.update_data(region_id=region_id)
    await callback_query.answer()
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML", reply_markup=update_education_info_ru)
    await UpdateEducationRU.new_district_id.set()
    
    data = await state.get_data()
    token = data['token']  # Use direct indexing for required data
    region_id = data['region_id']
    district_id_response = send_req.districts(token, int(region_id))  # Ensure it's awaited
    districts = district_id_response.json()  # Async call should be awaited
    # pprint(districts)
    buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"dist_{item['id']}")] for item in districts]
    districtsMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.answer("Выберите район:", reply_markup=districtsMenu)
    

@dp.callback_query_handler(lambda c: c.data.startswith('dist_'), state=UpdateEducationRU.new_district_id)
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
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML", reply_markup=update_education_info_ru)



@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'district', state=UpdateEducationRU.education_id)
async def update_district(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    token = data['token']  
    region_id = data['region_id']
    district_id_response = send_req.districts(token, int(region_id))  # Ensure it's awaited
    districts = district_id_response.json()  # Async call should be awaited
    # pprint(districts)
    buttons = [[InlineKeyboardButton(text=item['name_ru'], callback_data=f"dist_{item['id']}")] for item in districts]
    districtsMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.answer("Выберите район:", reply_markup=districtsMenu)

@dp.callback_query_handler(lambda c: c.data.startswith('dist_'), state=UpdateEducationRU.education_id)
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
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML", reply_markup=update_education_info_ru)

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'education_name', state=UpdateEducationRU.education_id)
async def update_education_name(callback_query: types.CallbackQuery, state: FSMContext):
    from aiogram import Bot, Dispatcher, types
    from data.config import BOT_TOKEN 
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    ic(type_your_edu_name_ru)
    await callback_query.message.answer(type_your_edu_name_ru)
    await UpdateEducationRU.institution_name.set()


@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'diploma', state=UpdateEducationRU.education_id)
async def update_diploma(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(example_diploma_message_ru)
    await UpdateEducationRU.file_diploma.set()

@dp.message_handler(content_types=['document'], state=UpdateEducationRU.file_diploma)
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

@dp.callback_query_handler(lambda mycallbackdata: mycallbackdata.data == 'certificate', state=UpdateEducationRU.education_id)
async def update_diploma(callback_query: types.CallbackQuery, state: FSMContext):

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

    await callback_query.message.answer(select_type_certificate_ru, reply_markup=certTypeMenu)
    await UpdateEducationRU.certificate_type.set()

# @dp.message_handler(state=UpdateEducationRU.certificate)
# async def update_certificate(message: types.Message, state: FSMContext):

@dp.callback_query_handler(lambda c: c.data.startswith('type_'), state=UpdateEducationRU.certificate_type)
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
    await UpdateEducationRU.get_certificate.set()  # Proceed to the next state
    # await message.answer(c)
    await callback_query.message.answer(saved_message_ru, parse_mode="HTML")
    await callback_query.message.answer(example_certification_message_ru, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(content_types=['document'], state=UpdateEducationRU.get_certificate)
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
    await message.answer(saved_message_ru, parse_mode="HTML", reply_markup=update_education_info_ru)
    

@dp.message_handler(state=UpdateEducationRU.institution_name)
async def update_institution_name(message: types.Message, state: FSMContext):
    institution_name_inputed = message.text
    if institution_name_inputed in ["📚 Посмотреть образовательную информацию", "📝 Редактировать образовательную информацию"]:
        await UpdateEducationRU.education_id.set()  # Move to the next state or modify as needed
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
        await message.answer(saved_message_ru, parse_mode="HTML", reply_markup=update_education_info_ru)

    await UpdateEducationRU.next()

@dp.message_handler(Text(equals="📚 Просмотр образовательной информации"), state="*")
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
        education_message = "<b>📚 Образовательная информация:</b>\n\n"
        if user_education.get('education_type_uz', None) is not None:
            education_message += (
                f"• <b>Тип образования:</b> {user_education.get('education_type_uz', 'Тип образования не найдено')}\n"
                f"• <b>Область:</b> {user_education.get('region_name_uz', 'Область не найден')}\n"
                f"• <b>Район:</b> {user_education.get('district_name_uz', 'Район не найден')}\n"
                f"• <b>Название учебного заведения:</b> {user_education.get('institution_name', 'Название учебного заведения не найдено')}\n"
            )
        elif pinfl_user_education['institution_name'] is not None:
            institution_type = pinfl_user_education.get('institution_type', 'Тип обучения не найден')
            if institution_type == 'school':
                institution_type = 'Школа'
            education_message += (
                # f"• <b>Daraja:</b> {pinfl_user_education.get('degree_name_uz', 'Daraja topilmadi')}\n"
                # f"• <b>Tamomlagan yil:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Tamomlagan yil topilmadi')}\n"
                # f"• <b> Mamlakat:</b> {pinfl_user_education.get('country', 'Shahar topilmadi')}\n"
                f"• <b>Город:</b> {pinfl_user_education.get('region', 'Город не найден')}\n"
                f"• <b>Район:</b> {pinfl_user_education.get('district', 'Район не найден')}\n"
                f"• <b>Тип образования:</b> {institution_type}\n"
                f"• <b>Название учебного заведения:</b> {pinfl_user_education.get('institution_name', 'Название учебного заведения не найдено')}\n"
            )

        # Sending the educational info message
        await message.answer(education_message, parse_mode="HTML", reply_markup=menu_ru)

        diploma_file = user_education.get('file')
        if diploma_file is not None:
            try:
                await message.answer_document(f"https://{domain_name}/{diploma_file[0]}", caption="Копия диплома, сертификата или справочного файла.")
            except Exception as e:
                print(f"Failed to send diploma file: {e}")
        elif pinfl_user_education:
            try:
                await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Копия диплома, сертификата или справочного файла.")
            except Exception as e:
                print(f"Failed to send diploma file: {e}")
            
        # Sending certification files if available

        ic(124)
        ic(certifications)
        for certification in certifications:
            if certification.get('file'):
                ic(127)
                certification_type = certification.get('certification_type', 'Тип сертификата не найден')
                try:
                    await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Копия сертификата: {certification_type.upper()}")
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
            education_message = "<b>📚 Образовательная информация:</b>\n\n"
            education_message += (
                f"• <b>Страна:</b> {user_education.get('country_name_uz', 'Страна не найдена')}\n"
                f"• <b>Название учебного заведения:</b> {user_education.get('institution_name', 'Название учебного заведения не найдено')}\n"
                f"""• <b>Направление:</b> {user_education.get('direction_name', "Направление не найдено")}\n"""
                f"• <b>Курс:</b> {user_education.get('which_course_now', 'Степень не найден')}-курс\n"
            )
            
            if pinfl_user_education is not None:
                if pinfl_user_education['pinfl_region_id'] is not None:
                    education_message += (
                        f"• <b>Степень:</b> {pinfl_user_education.get('degree_name_uz', 'Степень не найден')}\n"
                        f"• <b>Выпускной год:</b> {pinfl_user_education.get('pinfl_graduation_year', 'Выпускной год не найден')}\n"
                        f"• <b> Страна:</b> {pinfl_user_education.get('country', 'Страна не найденa')}\n"
                        f"• <b>Город:</b> {pinfl_user_education.get('region', 'Город не найден')}\n"
                        f"• <b>Район:</b> {pinfl_user_education.get('district', 'Район не найден')}\n"
                        f"• <b>Тип образования:</b> {pinfl_user_education.get('institution_type', 'Тип образования не найден')}\n"
                        f"• <b>Название учебного заведения:</b> {pinfl_user_education.get('institution_name', 'Название учебного заведения не найдено')}\n"
                )
            await message.answer(education_message, parse_mode="HTML", reply_markup=menu_ru)

            transcript_file = user_education.get('transcript_file')
            if transcript_file:
                try:
                    await message.answer_document(f"https://{domain_name}/{transcript_file}", caption="Копия файла транскрипта")
                except Exception as e:
                    print(f"Failed to send diploma file: {e}")
            elif pinfl_user_education:
                try:
                    await message.answer_document(f"https://{domain_name}/{pinfl_user_education['file'][0]}", caption="Копия диплома, сертификата или справочного файла.")
                except Exception as e:
                    print(f"Failed to send diploma file: {e}")
                
            # Sending certification files if available

            ic(124)
            if certifications is not None and certifications:
                for certification in certifications:
                    if certification.get('file'):
                        ic(127)
                        certification_type = certification.get('certification_type', 'Тип сертификата не найден')
                        try:
                            await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Копия сертификата: {certification_type.upper()}")
                        except Exception as e:
                            print(f"Failed to send certification file: {e}") 
    else:

        await message.answer("К сожалению, вашу информацию не удалось получить. Пожалуйста, выйдите из системы и войдите снова, чтобы получить еще раз.", reply_markup=menu_ru)
        # await message.answer("Kechirasiz, sizning ma'lumotlaringizni olish imkoni bo'lmadi. Iltimos,akkuntdan chiqib tizimga qayta kiring.", reply_markup=menu)


#TODO arizam
@dp.message_handler(Text(equals=["📁Заявление","📁заявление"]), state=PersonalDataRU.country_search)
async def my_application(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    ic('keldi arizaga')
    my_app = await send_req.my_applications(token=token)
    if not my_app:
        await message.answer("Информация о заявление не найдена.")
        return

    created_at = my_app.get('created_at', 'время создания не найдено')
    status = my_app.get('status', 'статус не найден')
    comments = my_app.get('comment', 'комментарий не найден')
    # status1 = my_app.get('status')
    # ic(status1)
    direction_name_uz = my_app.get('direction_name_uz', 'Образование не найдено')
    degree_name_uz = my_app.get('degree_name_uz', 'Уровень образования не найден')
    education_type_name_uz = my_app.get('education_type_name_uz','Тип обучения не найден' )
    education_language_name_uz = my_app.get('education_language_name_uz', 'Язык обучения не найден')
    tuition_fee = my_app.get('tuition_fee', 'Цена не найдена')
    date_obj = datetime.fromisoformat(created_at.rstrip("Z"))
    utc_timezone = pytz.timezone('UTC')
    desired_timezone = pytz.timezone('Asia/Tashkent')  # Replace 'Asia/Tashkent' with your desired timezone
    date_obj = utc_timezone.localize(date_obj).astimezone(desired_timezone)
    human_readable_date = date_obj.strftime("%Y-%m-%d %H:%M")
    if len(comments) >= 2:
        comments = comments[-1]
    if tuition_fee != 'Цена не найдена':
        formatted_fee = "{:,.0f}".format(tuition_fee).replace(',', '.')

    applicant_status_translations = {
    'PENDING': 'ожидается',
    'ACCEPTED': 'принято',
    'REJECTED': 'отклоненный',
    'EDIT-REJECT': 'Запрос на редактирование отклонен',
    'CALLED-EXAM': 'вызвали на экзамен',
    'EXAM-FEE': 'плата за экзамен была оплачена',
    'CAME-EXAM': 'пришел на экзамен',
    'MARKED': 'оценивается',
    'SUCCESS': 'успешный',
    'FAIL': 'не успешный',
    'CONTRACT': 'договор',
    'STUDENT': 'студент',
    'RECOMMENDED_STUDENT': 'рекомендуемый студент'
    }
    comment = comments.get('comment', 'комментарий не найден')
    comment_time = comments.get('created_at', 'время комментария не найдено')
    if comment_time != 'время комментария не найдено':
        comment_time = convert_time(comment_time)
    status_name = applicant_status_translations.get(status.upper(), "Не найдено")
    color = 'blue' if comment == 'комментарий не найден' else 'red'
    if color == 'blue':
        color = "🔵"
    elif color == 'red':
        color = "🔴"
    response_message = (
        f"<b>Детали Заявления:</b>\n"
        f"Время создания: {human_readable_date}\n"
        f"Статус:   <b>{status_name}</b>\n"
        f"Направление: {direction_name_uz}\n"
        f"Степень: {degree_name_uz}\n"
        f"Тип образования: {education_type_name_uz}\n"
        f"Язык обучения: {education_language_name_uz}\n"
        f"Стоимость обучения: {formatted_fee} so'm\n"
        f"Время комментирования {escape_markdown(comment_time)}"
        f" {color} Объяснение: {escape_markdown(comment)}\n"
    )
    await message.answer(response_message, parse_mode='HTML')


@dp.message_handler(Text(equals="📁Заявление"), state="*")
async def my_application(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    ic('keldi arizaga')
    my_app = await send_req.my_applications(token=token)
    ic(my_app)
    if not my_app:
        await message.answer("Информация о заявление не найдена.")
        return

    created_at = my_app.get('created_at', 'время создания не найдено')
    status = my_app.get('status', 'статус не найден')
    direction_name_uz = my_app.get('direction_name_uz', 'Направление не найдено')
    degree_name_uz = my_app.get('degree_name_uz', 'Уровень образования не найден')
    education_type_name_uz = my_app.get('education_type_name_uz','Talim darajasi topilmadi' )
    education_language_name_uz = my_app.get('education_language_name_uz', 'Язык обучения не найден')
    tuition_fee = my_app.get('tuition_fee', 'Цена не найдена')
    comments = my_app.get('comment', [])
    date_obj = datetime.fromisoformat(created_at.rstrip("Z"))
    utc_timezone = pytz.timezone('UTC')
    desired_timezone = pytz.timezone('Asia/Tashkent')  # Replace 'Asia/Tashkent' with your desired timezone
    date_obj = utc_timezone.localize(date_obj).astimezone(desired_timezone)
    human_readable_date = date_obj.strftime("%Y-%m-%d %H:%M")
    if len(comments) >= 2:
        comments = comments[-1]
    if tuition_fee != 'Цена не найдена':
        formatted_fee = "{:,.0f}".format(tuition_fee).replace(',', '.')

    applicant_status_translations = {
    'PENDING': 'ожидается',
    'ACCEPTED': 'принял',
    'REJECTED': 'отклоненный',
    'EDIT-REJECT': 'Запрос на редактирование отклонен',
    'CALLED-EXAM': 'вызвали на экзамен',
    'EXAM-FEE': 'плата за экзамен оплачена',
    'CAME-EXAM': 'пришел на экзамен',
    'MARKED': 'оценивается',
    'SUCCESS': 'успешный',
    'FAIL': 'не успешный',
    'CONTRACT': 'договор',
    'STUDENT': 'студент',
    'RECOMMENDED_STUDENT': 'рекомендуемый студент'
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
        comment = 'комментарий не найден'
        comment_time = 'время комментария не найдено'
    status_name = applicant_status_translations.get(status.upper(), "Не найдено")

    color = 'blue' if comment == 'комментарий не найден' else 'red'
    if color == 'blue':
        color = "🔵"
    elif color == 'red':
        color = "🔴"    
    response_message = (
        f"*Детали заявления:*\n"
        f"Время создания: {escape_markdown(human_readable_date)}\n"
        f"Статус:   *{escape_markdown(status_name)}*\n"
        f"Направление: {escape_markdown(direction_name_uz)}\n"
        f"Степень: {escape_markdown(degree_name_uz)}\n"
        f"Тип образования: {escape_markdown(education_type_name_uz)}\n"
        f"Язык обучения: {escape_markdown(education_language_name_uz)}\n"
        f"Стоимость обучения: {escape_markdown(formatted_fee)} so'm\n\n"
        f"Время комментирования: {escape_markdown(comment_time)}\n"
        f"{color} *Комментарий:* {escape_markdown(comment)}\n"
    )
    await message.answer(response_message, parse_mode='MarkdownV2')