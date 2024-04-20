from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup
from keyboards.default.registerKeyBoardButton import menu, application, ask_delete_account,exit_from_account
from states.personalData import PersonalData, EducationData
from loader import dp
from utils import send_req
from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic
from data.config import domain_name
from datetime import datetime


start_button = KeyboardButton('/start')  # The text on the button
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)

@dp.message_handler(Text(equals="🗑Akkauntni o'chirish"), state=EducationData.menu)
async def delete_account_prompt(message: types.Message, state: FSMContext):
    await message.answer("Akkaunt o'chirilsinmi?", reply_markup=ask_delete_account)

@dp.message_handler(Text(equals="Ha, akkauntni o'chirish"), state=EducationData.menu)
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


@dp.message_handler(Text(equals="Akkauntdan chiqish"), state=EducationData.menu)
async def ask_exit_menu(message: Message, state: FSMContext):
    await message.answer("Akkauntdan chiqishni istaysizmi?", reply_markup=exit_from_account)

@dp.message_handler(Text(equals="Ha, Akkauntdan chiqish"), state="*")
async def exit_menu(message: Message, state: FSMContext):
    await state.update_data(token=None)
    await state.update_data(start_count=0)
    await message.answer('Siz akkauntdan chiqdingiz\nStart tugmasini bosib qaytadan tizimga kiring', reply_markup=start_keyboard)

@dp.message_handler(Text(equals="Bekor qilish"), state=EducationData.menu)
async def stay_menu(message: Message, state: FSMContext):
    await message.answer("Asosiy sahifa", reply_markup=menu)

@dp.message_handler(Text(equals="ℹ️Shaxsiy ma'lumotlar"), state=EducationData.menu)
async def my_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    if token:
        personal_info = await send_req.application_forms_me(token)
        ic(personal_info)
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

@dp.message_handler(Text(equals="📚Ta'lim ma'lumotlari"), state=EducationData.menu)
async def education_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    if token:
        education_info = await send_req.application_forms_me(token)
        # ic(education_info)
        user_education = education_info.get('user_education', {})
        certifications = education_info.get('certifications', [])
        pinfl_user_education = education_info.get('pinfl_user_education', {})
        ic(education_info)
        ic(certifications)
        ic(pinfl_user_education)
        # Constructing the education message
        education_message = "<b>📚 Ta'lim Ma'lumotlari:</b>\n\n"
        education_message += (
            f"• <b>Ta'lim turi:</b> {user_education.get('education_type_uz', 'Talim turi topilmadi')}\n"
            f"• <b>Viloyat:</b> {user_education.get('region_name_uz', 'Viloyat topilmadi')}\n"
            f"• <b>Tuman:</b> {user_education.get('district_name_uz', 'Tuman topilmadi')}\n"
            f"• <b>O'quv muassasasi nomi:</b> {user_education.get('institution_name', 'Institut nomi topilmadi')}\n"
        )
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

        # Sending the educational info message
        await message.answer(education_message, parse_mode="HTML")


        # Sending the diploma file if available
        diploma_file = user_education.get('file')
        if diploma_file:
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
        for certification in certifications:
            if certification.get('file'):
                ic(127)
                certification_type = certification.get('certification_type', 'Sertifikat turi topilmadi')
                try:
                    await message.answer_document(f"https://{domain_name}/{certification['file']}", caption=f"Sertifikat nusxasi: {certification_type.upper()}")
                except Exception as e:
                    print(f"Failed to send certification file: {e}")
            
    else:
        # Handle the case where the token is None or invalid
        await message.answer("Kechirasiz, sizning ma'lumotlaringizni olish imkoni bo'lmadi. Iltimos, qayta urinib ko'ring.")
@dp.message_handler(Text(equals="📁Arizalar"), state=EducationData.menu)
async def my_application(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
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
    date_obj = datetime.fromisoformat(created_at.rstrip("Z"))
    human_readable_date = date_obj.strftime("%Y-%m-%d %H:%M")
    if tuition_fee != 'Narxi topilmadi':
        formatted_fee = "{:,.0f}".format(tuition_fee).replace(',', '.')

    applicant_status_translations = {
    'PENDING': 'kutilmoqda',
    'ACCEPTED': 'qabul qilingan',
    'REJECTED': 'rad etilgan',
    'EDIT_REJECT': 'tahrirlash rad etildi',
    'CALLED_EXAM': 'imtihonga chaqirilgan',
    'EXAM_FEE': 'imtihon uchun to\'lov to\'langan',
    'CAME_EXAM': 'imtihonga kelgan',
    'MARKED': 'baholangan',
    'SUCCESS': 'muvaffaqiyatli',
    'FAIL': 'muvaqqiyatsiz',
    'CONTRACT': 'shartnoma',
    'STUDENT': 'talaba',
    'RECOMMENDED_STUDENT': 'tavsiya etilgan talaba'
    }
    status_name = applicant_status_translations.get(status.upper(), "Topilmadi")
    response_message = (
        f"<b>Ariza Tafsilotlari:</b>\n"
        f"Yaratilgan vaqti: {human_readable_date}\n"
        f"Holati:   <b>{status_name}</b>\n"
        f"Yo'nalishi: {direction_name_uz}\n"
        f"Darajasi: {degree_name_uz}\n"
        f"Ta'lim turi: {education_type_name_uz}\n"
        f"Ta'lim til: {education_language_name_uz}\n"
        f"Ta'lim narix: {formatted_fee} so'm"
    )
    await message.answer(response_message, parse_mode='HTML')