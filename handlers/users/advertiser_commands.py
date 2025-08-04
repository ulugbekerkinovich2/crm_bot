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
from icecream import ic
import datetime
from keyboards.default.adminMenuKeyBoardButton import adminConfirm, adminMenu
from aiogram.types import ReplyKeyboardRemove

from aiogram.types import Message, MessageEntity
from collections import defaultdict
from typing import List
def wrap_entity(text: str, types: List[str], url: str = None) -> str:
    for t in reversed(types):
        if t == "bold":
            text = f"<b>{text}</b>"
        elif t == "italic":
            text = f"<i>{text}</i>"
        elif t == "underline":
            text = f"<u>{text}</u>"
        elif t == "strikethrough":
            text = f"<s>{text}</s>"
        elif t == "code":
            text = f"<code>{text}</code>"
        elif t == "pre":
            text = f"<pre>{text}</pre>"
        elif t == "text_link" and url:
            text = f"<a href='{url}'>{text}</a>"
    return text


def get_html_text_from_message(message: Message) -> str:
    # text = message.caption or ""
    text = message.text or message.caption or ""
    entities = message.caption_entities or []

    if not text or not entities:
        return text

    # Entity larni boshlanish joyi bo‘yicha guruhlaymiz
    starts = defaultdict(list)
    ends = defaultdict(list)

    for entity in entities:
        starts[entity.offset].append(entity)
        ends[entity.offset + entity.length].append(entity)

    result = ""
    active_entities = []
    i = 0

    while i < len(text):
        # Entity tugagan bo‘lsa, ro‘yxatdan o‘chiramiz
        if i in ends:
            for e in ends[i]:
                if e in active_entities:
                    active_entities.remove(e)

        # Entity boshlansa, ro‘yxatga qo‘shamiz
        if i in starts:
            for e in starts[i]:
                active_entities.append(e)

        # Nechta harfni keyingi o‘zgarishgacha olish kerakligini aniqlaymiz
        next_change = min(
            [pos for pos in list(starts.keys()) + list(ends.keys()) if pos > i],
            default=len(text)
        )
        chunk = text[i:next_change]

        if active_entities:
            types = [e.type for e in active_entities]
            url = next((e.url for e in active_entities if e.type == "text_link"), None)
            result += wrap_entity(chunk, types, url)
        else:
            result += chunk

        i = next_change

    return result


#TODO for all users
@dp.message_handler(text="📝 Matn yuborish")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        await message.answer("Reklama xabarini yuboring, ushbu habar barcha user larga boradi!!!")
        await User.get_command.set()

@dp.message_handler(state=User.get_command)
async def preview_advertisement(message: types.Message, state: FSMContext):
    # ic(99, message)
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        text = message.text
        content_type = message.content_type
        ic(103, content_type)
        if content_type == types.ContentType.TEXT:
            text = get_html_text_from_message(message)
            ic(107, text)
        else:
            text = message.caption or message.text
        await state.update_data(reklama={"caption": text, "type": types.ContentType.TEXT})
        await message.answer(
            f"<b>Reklama ko'rinishi:</b>\n\n{text}\n\nQuyidagi tugmalar orqali tasdiqlang:",
            parse_mode='HTML',
            reply_markup=adminConfirm
        )
        await User.confirm_reklama.set()




@dp.message_handler(text="🖼 Rasm yuborish")  
async def bot_starts(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.from_user.id
    if chat_id in admin_ids:
        await message.answer("Reklama rasmini matni bilan yuboring, ushbu habar barcha userlarga boradi")
        await User.reklama_admin_image_all.set()

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT], state=User.reklama_admin_image_all)
async def handle_image_and_text(message: types.Message, state: FSMContext):
    if message.from_user.id not in admin_ids:
        return

    # Faqat text kelsa ruxsat bermaymiz
    if message.content_type == types.ContentType.TEXT:
        await message.answer("Iltimos, rasm bilan birga caption yuboring.")
        return

    # Rasm va caption keldi
    elif message.content_type == types.ContentType.PHOTO:
        photo_file_id = message.photo[-1].file_id
        caption = get_html_text_from_message(message)

        # Saqlaymiz
        await state.update_data(reklama={
            'type': 'photo',
            'file_id': photo_file_id,
            'caption': caption
        })

        await message.answer_photo(photo=photo_file_id, caption=f"<b>Yuboriladigan rasm:</b>\n\n{caption}", parse_mode="HTML")
        await message.answer("❓ Ushbu reklamani yuborishni tasdiqlaysizmi?", reply_markup=adminConfirm)
        await User.confirm_reklama.set()





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
    await message.answer(text)

async def process_image1(message: types.Message, photo_file_id: str, caption: str, state: FSMContext):
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
            parse_mode="HTML",
            reply_markup=adminMenu
        )
        await state.finish()


#TODO video uchun
@dp.message_handler(text="📹 Video yuborish")
async def bot_starts(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Reklama videosini matni bilan yuboring, ushbu reklama hammaga boradi")
    await User.reklama_admin_video_or_image_all.set()


@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT], state=User.reklama_admin_video_or_image_all)
async def handle_media_and_text(message: types.Message, state: FSMContext):
    content_type = message.content_type
    content_type = message.content_type
    if content_type == types.ContentType.VIDEO:
        caption = get_html_text_from_message(message)
    else:
        caption = message.caption or message.text
    ic(229, caption)
    data = {
        'type': content_type,
        'caption': caption
    }

    if content_type == types.ContentType.VIDEO:
        data['file_id'] = message.video.file_id

    elif content_type == types.ContentType.PHOTO:
        data['file_id'] = message.photo[-1].file_id

    await state.update_data(reklama=data)
    ic(data)
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
                # send_req.update_user(user['id'], user['chat_id'], user['firstname'], user['lastname'], user['bot_id'], user['username'], 'active', user['created_at'])
                count += 1
            except Exception as e:
                failed += 1
                # send_req.update_user(user['id'], user['chat_id'], user['firstname'], user['lastname'], user['bot_id'], user['username'], 'blocked', user['created_at'])

        await message.answer(
            f"📢 <b>Reklama natijasi</b>\n\n"
            f"✅ Yuborildi: <b>{count:,}</b> ta\n"
            f"❌ Xatolik: <b>{failed:,}</b> ta",
            parse_mode="HTML",
            reply_markup=adminMenu
        )
        await state.finish()

    elif message.text == '❌ Bekor qilish':
        await message.answer("❌ Reklama yuborish bekor qilindi.", reply_markup=adminMenu)
        await state.finish()

    else:
        await message.reply("Iltimos, faqat quyidagi tugmalardan birini tanlang: ✅ Yuborish yoki ❌ Bekor qilish.")


@dp.message_handler(text="📊 Statistika")  # Assuming you have a function or logic to check if the user is an admin
async def bot_starts(message: types.Message, state: FSMContext):
    await state.finish()
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