from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.default.registerKeyBoardButton import menu, menu_full, application, ask_delete_account,exit_from_account, update_personal_info,finish_edit,update_education_info
from keyboards.inline.menukeyboards import update_personal_info_inline,edit_user_education_inline,edit_user_education_transfer_inline
import re
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
from data.config import university_id as UNIVERSITY_ID,exam_link
from handlers.users import upload,collect_data
from datetime import datetime, timedelta
from states.advertiser_command import GranState
from utils.send_req import grant_languages, grant_directions, grant_applicant
from handlers.users.register import saved_message,select_region,type_your_edu_name,example_diploma_message,wait_file_is_loading,select_type_certificate,example_certification_message,not_found_country,search_university,select_one
start_button = KeyboardButton('/start')  # The text on the button
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)
escape_markdown = send_req.escape_markdown
convert_time = send_req.convert_time
from keyboards.default import registerKeyBoardButton, adminMenuKeyBoardButton

@dp.message_handler(Text(equals='🔙 Orqaga'), state='*')
async def admin_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.branch_uz)

@dp.message_handler(Text(equals='🔙 Orqaga*'), state='*')
async def admin_commandBack(message: types.Message, state: FSMContext):
    await state.finish()
    ic('admin command')
    await message.answer("Admin Reklama paneliga xush kelibsiz", reply_markup=adminMenuKeyBoardButton.adminMenu)


@dp.message_handler(Text(equals='📢 Reklama yuborish'), state='*')
async def admin_commandAds(message: types.Message, state: FSMContext):
    await state.finish()
    ic('admin command')
    await message.answer("Reklama paneli", reply_markup=adminMenuKeyBoardButton.adsMenu)

# 1️⃣ — Bosqich: Tillarni chiqarish
@dp.message_handler(state=GranState.language)
async def show_languages(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')

    if not token:
        await message.answer("❌ Token topilmadi. Iltimos, avval tizimga kiring.")
        return

    languages = await grant_languages(token)
    if isinstance(languages, dict) and languages.get("error"):
        await message.answer(f"❌ Xatolik: {languages['error']}")
        return

    buttons = [
        [InlineKeyboardButton(text=item['name_uz'], callback_data=f"lan_{item['id']}")]
        for item in languages
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        "Daraja: Bakalavr\nTa'lim shakli: Kunduzgi\nTilni tanlang:",
        reply_markup=markup
    )
    await GranState.after_lang.set()


# 2️⃣ — Bosqich: Til tanlash va yo‘nalishlarni chiqarish
@dp.callback_query_handler(lambda c: c.data.startswith('lan_'), state=GranState.after_lang)
async def language_selected(call: types.CallbackQuery, state: FSMContext):
    language_id = call.data.split('lan_')[1]
    await state.update_data(language_id=language_id)

    data = await state.get_data()
    token = data.get('token')

    # Eski til tanlash menyusini o‘chirib tashlaymiz
    await call.message.delete()

    # Til bo‘yicha filtrlangan yo‘nalishlar
    directions = await grant_directions(token, education_language_id=language_id)
    if isinstance(directions, dict) and directions.get("error"):
        await call.message.answer(f"❌ Xatolik: {directions['error']}")
        return

    buttons = [
        [InlineKeyboardButton(text=item['name_uz'], callback_data=f"dir_{item['id']}")]
        for item in directions
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await call.message.answer(
        "Daraja: Bakalavr\nTa'lim shakli: Kunduzgi\nYo'nalishni tanlang:",
        reply_markup=markup
    )

    await GranState.direction.set()


@dp.callback_query_handler(lambda c: c.data.startswith('dir_'), state=GranState.direction)
async def direction_selected(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')
    language_id = data.get('language_id')
    direction_id = call.data.split('dir_')[1]

    await state.update_data(direction_id=direction_id)

    # Eski yo‘nalish tanlash menyusini o‘chirib tashlaymiz
    await call.message.delete()

    res = grant_applicant(token, 1, direction_id, language_id, 1)
    ic(res)

    payment_link = "https://my.click.uz/services/pay?service_id=77482&merchant_id=27574&amount=50000&transaction_param=CRM75145&return_url=https://grant.aifu.uz/profile/application-status"
    text = (
        "💳 <b>Imtihon uchun to'lov</b>\n"
        "💵 To'lov summasi: <b>50 000 UZS</b>\n\n"
        f"<a href='{payment_link}'>✅ To‘lovni amalga oshirish</a>"
    )

    await call.message.answer(text, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())


