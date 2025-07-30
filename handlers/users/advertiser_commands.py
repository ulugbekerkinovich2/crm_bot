from aiogram import types, Bot
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
import aiogram.types
import keyboards.default
from loader import dp, bot
import asyncio
from states.advertiser_command import User
from data.config import admin_ids
from utils import send_req
# from filters.custom import IsAdminFilter
from icecream import ic
import datetime
from keyboards.default.adminMenuKeyBoardButton import adminConfirm, adminMenu
from aiogram.types import ReplyKeyboardRemove



#TODO for all users
@dp.message_handler(text="📝 Matn yuborish")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        await message.answer("Reklama xabarini yuboring, ushbu habar barcha user larga boradi!!!")
        await User.get_command.set()

@dp.message_handler(state=User.get_command)
async def preview_advertisement(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        text = message.text

        await state.update_data(reklama={"caption": text, "type": types.ContentType.TEXT})
        await message.answer(
            f"<b>Reklama ko'rinishi:</b>\n\n{text}\n\nQuyidagi tugmalar orqali tasdiqlang:",
            parse_mode='HTML',
            reply_markup=adminConfirm
        )
        await User.confirm_reklama.set()






@dp.message_handler(text="🖼 Rasm yuborish")  
async def bot_starts(message: types.Message):
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        await message.answer("Reklama rasmini matni bilan yuboring, ushbu habar barcha userlarga boradi")
        await User.reklama_admin_image_all.set()

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT], state=User.reklama_admin_image_all)
async def handle_image_and_text(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        if message.content_type == types.ContentType.TEXT:
            
            # Handle text message
            text = message.text
            await process_text(message, text)

        elif message.content_type == types.ContentType.PHOTO:
            # Handle image message
            photo_file_id = message.photo[-1].file_id
            caption = message.caption
            await process_image(message, photo_file_id, caption, state)

async def process_image(message: types.Message, photo_file_id: str, caption: str, state: FSMContext):
    # Process the image message
    # print("Photo file ID:", photo_file_id)
    # print("Caption:", caption)
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        all_users = send_req.get_all_users()  # Assuming you get all users from somewhere
        failed = 0
        count = 0
        for user_info in all_users:
            user_id = user_info.get('chat_id')
            ic(11, user_id)
            try:
            # Parse the text as Markdown to make links clickable
                await bot.send_photo(user_id, photo=photo_file_id, caption=caption, parse_mode="HTML")
                
                # Add a small delay to avoid being banned for spam
                await asyncio.sleep(1.2)
                
                send_req.update_user(user_info['id'], user_info['chat_id'], user_info['firstname'], user_info['lastname'],user_info['bot_id'], user_info['username'], 'active', user_info['created_at'])
                count += 1
            except Exception as e:
                failed += 1
                send_req.update_user(int(user_info.get('id')), user_info['chat_id'], user_info['firstname'], user_info['lastname'],user_info['bot_id'], user_info['username'], 'blocked',user_info['created_at'])
                print(f"Failed to send message to user {user_id}: {e}")
        await message.reply(
            f"📢 <b>Reklama tarqatish natijasi</b>\n\n"
            f"✅ Yuborildi: <b>{count:,}</b> ta foydalanuvchiga\n"
            f"❌ Yuborilmadi: <b>{failed:,}</b> ta foydalanuvchiga",
            parse_mode="HTML",
            reply_markup=adminMenu
        )
        await state.finish()











@dp.message_handler(text="/reklama_admin_image_text_for_admins")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        await message.answer("Reklama rasmini yuboring, ushbu reklama adminlarga boradi")
        await User.reklama_admin_image_text_for_admins.set()

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT], state=User.reklama_admin_image_text_for_admins)
async def handle_image_and_text(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        if message.content_type == types.ContentType.TEXT:

            text = message.text
            await process_text(message, text)

        elif message.content_type == types.ContentType.PHOTO:
            # Handle image message
            photo_file_id = message.photo[-1].file_id
            caption = message.caption
            await process_image1(message, photo_file_id, caption, state)

async def process_text(message: types.Message, text: str):
    # Process the text message
    # print("Text:", text)
    await message.answer(text)

async def process_image1(message: types.Message, photo_file_id: str, caption: str, state: FSMContext):
    # Process the image message
    # print("Photo file ID:", photo_file_id)
    # print("Caption:", caption)
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        fail_count = 0
        count = 0
        for user_id in admin_ids:
            ic(user_id)
            # user_id = user_info.get('chat_id')
            try:
                await bot.send_photo(user_id, photo=photo_file_id, caption=caption)
                # Add a small delay to avoid being banned for spam
                await asyncio.sleep(1.2)
                count += 1
                # send_req.update_user(user_id['id'], user_id['chat_id'], user_id['firstname'], user_id['lastname'],user_id['bot_id'], user_id['username'], 'active', user_id['created_at'])
            except Exception as e:
                fail_count += 1
                # send_req.update_user(int(user_id.get('id')), user_id['chat_id'], user_id['firstname'], user_id['lastname'],user_id['bot_id'], user_id['username'], 'blocked',user_id['created_at'])
                print(f"Failed to send message to user {user_id}: {e}")

        await message.reply(
            f"📢 <b>Adminlarga reklama yuborish natijasi</b>\n\n"
            f"✅ Yuborildi: <b>{count:,}</b> ta admin\n"
            f"❌ Yuborilmadi: <b>{fail_count:,}</b> ta admin",
            parse_mode="HTML"
        )
        await state.finish()








#TODO video uchun
@dp.message_handler(text="📹 Video yuborish")
async def bot_starts(message: types.Message):
    await message.answer("Reklama videosini matni bilan yuboring, ushbu reklama hammaga boradi")
    await User.reklama_admin_video_or_image_all.set()


@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT], state=User.reklama_admin_video_or_image_all)
async def handle_media_and_text(message: types.Message, state: FSMContext):
    content_type = message.content_type
    caption = message.caption if message.caption else message.text
    print(315, caption)
    data = {
        'type': content_type,
        'caption': caption
    }

    if content_type == types.ContentType.VIDEO:
        data['file_id'] = message.video.file_id

    elif content_type == types.ContentType.PHOTO:
        data['file_id'] = message.photo[-1].file_id

    await state.update_data(reklama=data)
    # await message.answer(data)
    await message.answer("📨 Reklama quyidagicha yuboriladi. Tasdiqlaysizmi?", reply_markup=adminConfirm)
    await User.confirm_reklama.set()



@dp.message_handler(state=User.confirm_reklama)
async def confirm_sending(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ic(281, data)
    reklama = data.get('reklama')
    ic(282, reklama)
    if message.text == '✅ Yuborish':
        all_users = send_req.get_all_users()
        count, failed = 0, 0

        for user in all_users:
            try:
                if reklama['type'] == types.ContentType.TEXT:
                    await bot.send_message(user['chat_id'], reklama['caption'])
                elif reklama['type'] == types.ContentType.PHOTO:
                    await bot.send_photo(user['chat_id'], reklama['file_id'], caption=reklama['caption'])
                elif reklama['type'] == types.ContentType.VIDEO:
                    await bot.send_video(user['chat_id'], reklama['file_id'], caption=reklama['caption'])
                await asyncio.sleep(1.2)
                send_req.update_user(user['id'], user['chat_id'], user['firstname'], user['lastname'], user['bot_id'], user['username'], 'active', user['created_at'])
                count += 1
            except Exception as e:
                failed += 1
                send_req.update_user(user['id'], user['chat_id'], user['firstname'], user['lastname'], user['bot_id'], user['username'], 'blocked', user['created_at'])

        await message.answer(
            f"📢 <b>Reklama natijasi</b>\n\n"
            f"✅ Yuborildi: <b>{count:,}</b> ta\n"
            f"❌ Xatolik: <b>{failed:,}</b> ta",
            parse_mode="HTML",
            reply_markup=adminMenu
        )
        await state.finish()

    elif message.text == '❌ Bekor qilish':
        await message.answer("❌ Reklama yuborish bekor qilindi.", reply_markup=ReplyKeyboardRemove())
        await state.finish()

    else:
        await message.reply("Iltimos, faqat quyidagi tugmalardan birini tanlang: ✅ Yuborish yoki ❌ Bekor qilish.")


@dp.message_handler(text="📊 Statistika")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count_of_users = send_req.get_all_users()
    active = 0
    blocked = 0
    for user in count_of_users:
        if user['status'] == 'active':
            active += 1
        elif user['status'] == 'blocked':
            blocked += 1
    response_message = (
        f"📊 <b>Bot foydalanuvchi statistikasi</b>\n\n"
        f"📅 Sana: <b>{time}</b>\n"
        f"👥 Umumiy foydalanuvchilar: <b>{len(count_of_users):,}</b> ta\n"
        f"✅ Aktiv foydalanuvchilar: <b>{active:,}</b> ta\n"
        f"🚫 Bloklangan foydalanuvchilar: <b>{blocked:,}</b> ta"
    )
    await message.answer(response_message)