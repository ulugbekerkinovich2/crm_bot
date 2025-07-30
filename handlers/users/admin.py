from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from keyboards.default.registerKeyBoardButton import menu, menu_full, application, ask_delete_account,exit_from_account, update_personal_info,finish_edit,update_education_info
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
from data.config import university_id as UNIVERSITY_ID,exam_link
from handlers.users import upload,collect_data
from datetime import datetime, timedelta
from handlers.users.register import saved_message,select_region,type_your_edu_name,example_diploma_message,wait_file_is_loading,select_type_certificate,example_certification_message,not_found_country,search_university,select_one
start_button = KeyboardButton('/start')  # The text on the button
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)
escape_markdown = send_req.escape_markdown
convert_time = send_req.convert_time
from keyboards.default import registerKeyBoardButton, adminMenuKeyBoardButton
@dp.message_handler(Text(equals='🔙 Orqaga'), state='*')
async def admin_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🏠Asosiy sahifa", reply_markup=registerKeyBoardButton.language)

@dp.message_handler(Text(equals='🔙 Orqaga*'), state='*')
async def admin_commandBack(message: types.Message, state: FSMContext):
    await state.finish()
    ic('admin command')
    await message.answer("Admin Reklama paneliga xush kelibsiz", reply_markup=adminMenuKeyBoardButton.adminMenu)


@dp.message_handler(Text(equals='📢 Reklama yuborish'), state='*')
async def admin_commandAds(message: types.Message, state: FSMContext):
    await state.finish()
    ic('admin command')
    await message.answer("🏠Asosiy sahifa", reply_markup=adminMenuKeyBoardButton.adsMenu)