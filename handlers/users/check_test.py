from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from aiogram.types import ContentType, InputFile
import os
import pandas as pd
import json

# 📌 Faqat quyidagi adminlarga yuklash ruxsati
ALLOWED_ADMINS = [7432861733, 935920479]

# 📂 JSON saqlanadigan fayl nomi
DB_PATH = "database.json"

# 📸 "📃Test natijasini bilish" komanda bosilganda
@dp.message_handler(Text(equals="📃Test natijasini bilish"))
async def start(message: types.Message):
    photo = InputFile("example_test.jpg")
    await message.answer_photo(
        photo=photo,
        caption="<b>Telefon raqam yuboring:\nNamuna: 901234567</b>",
        parse_mode="HTML"
    )

# 🔁 JSON ga yozish (full duplicate check bilan)
def append_to_json(data):
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            current = json.load(f)
    else:
        current = []

    for existing in current:
        if all(str(existing.get(k)) == str(data.get(k)) for k in data.keys()):
            return False  # ❌ To‘liq bir xil — qo‘shmaymiz

    current.append(data)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    return True

# 🧾 Admin .xlsx yuklasa
@dp.message_handler(content_types=ContentType.DOCUMENT)
async def handle_xlsx(message: types.Message):
    if message.from_user.id not in ALLOWED_ADMINS:
        return await message.answer("❌ Sizga bu amalni bajarish ruxsat etilmagan.")

    file = await message.document.download()
    df = pd.read_excel(file.name)

    required_columns = [
        "phone", "full_name", "type_direction", "direction",
        "subject_1", "subject_2", "subject_1_corrects", "subject_1_score",
        "subject_2_corrects", "subject_2_score", "mandatory_correct", "mandatory_score", "overall"
    ]

    if not all(col in df.columns for col in required_columns):
        return await message.answer("❌ Excel faylda kerakli ustunlar yo‘q.")

    added = 0
    for _, row in df.iterrows():
        row_dict = {col: row[col] for col in required_columns}
        if append_to_json(row_dict):
            added += 1

    await message.answer(f"✅ {added} ta yangi natija muvaffaqiyatli qo‘shildi.")

# 📱 User telefon raqamini yuborsa
@dp.message_handler(lambda msg: msg.text.isdigit() and len(msg.text) >= 7)
async def check_result(message: types.Message):
    phone = message.text.strip()

    if not os.path.exists(DB_PATH):
        return await message.answer("❌ Hali hech qanday natija mavjud emas.")

    with open(DB_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)

    results = [r for r in records if str(r["phone"]).endswith(phone)]

    if not results:
        return await message.answer("❌ Siz kiritgan raqam bo‘yicha natija topilmadi.")

    for r in results:
        msg = (
            f"📊 <b>Natijangiz</b>\n"
            f"👤 <b>F.I.SH:</b> {r['full_name']}\n"
            f"📚 <b>Yo’nalish:</b> {r['direction']}\n"
            f"—" + "–" * 20 + "\n"
            f"📘 <b>Ixtisoslik fanlari:</b>\n"
            f"➊ {r['subject_1']} : {r['subject_1_corrects']}/30 = {r['subject_1_score']}/93\n"
            f"➋ {r['subject_2']} : {r['subject_2_corrects']}/30 = {r['subject_2_score']}/63\n"
            f"📙 <b>Majburiy fanlar:</b>\n"
            f"📎 Ona tili, O'zbekiston Tarixi, Matematika : {r['mandatory_correct']}/30 = {r['mandatory_score']}/33\n"
            f"—" + "–" * 20 + "\n"
            f"🏁 <b>Umumiy natija:</b> {r['overall']}/189\n\n"
            f"📢 <b>Rasman a'zo bo‘ling va yangiliklardan xabardor bo‘ling:</b>\n"
            f"🌐 <a href='https://aifu.uz'>🌍 aifu.uz</a>\n"
            f"📝 <a href='https://qabul.aifu.uz'>📥 qabul.aifu.uz</a>\n"
            f"🤖 <a href='https://t.me/aifu_qabul_bot'>@aifu_qabul_bot</a>"
        )
        await message.answer(msg, parse_mode="HTML")
