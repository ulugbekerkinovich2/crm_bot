from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from aiogram.types import ContentType, InputFile
import os
import pandas as pd
import json
import qrcode
from PIL import Image, ImageDraw, ImageFont
import requests


import os
from PIL import Image, ImageDraw, ImageFont



def generate_certificate(user_name, score, output_path, qr_url):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, "new_image.png")

        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)

        # font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        font = ImageFont.truetype(font_path, size=100)
        font_ = ImageFont.truetype(font_path, size=66)

        draw.text((950, 1000), user_name, fill="black", font=font)
        draw.text((1270, 760), f'{score} ball', fill="black", font=font_)

        qr = qrcode.make(qr_url).resize((360, 360))
        img.paste(qr, (1900, 1800))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)

        print(f"✅ Sertifikat saqlandi: {output_path}")
        return os.path.abspath(output_path)
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None






def upload_certificate(png_path, final_filename):
    try:
        pdf_path = os.path.join("output", f"{final_filename}.pdf")
        img = Image.open(png_path).convert("RGB")
        img.save(pdf_path)

        url = "https://qr.misterdev.uz/api/upload/"
        with open(pdf_path, "rb") as f:
            files = {"files": (f"{final_filename}.pdf", f, "application/pdf")}
            response = requests.post(url, files=files)

        if response.status_code == 201:
            file_url = f"https://qr.misterdev.uz/media/files/{final_filename}.pdf"
            return {
                "pdf_path": pdf_path,
                "qr_url": file_url
            }
        else:
            raise Exception(f"API error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Yuklash xatoligi: {e}")
        return None





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
def generate_filename(full_name):
    clean = full_name.replace(" ", "_").replace("'", "")
    return f"{clean}_sertifikat"

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
        # 🟢 Natija xabari
        msg_text = (
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
        await message.answer(msg_text, parse_mode="HTML")

        # 🎓 Sertifikat faqat 70+ bo‘lganlar uchun
        if float(r['overall']) >= 70:
            await message.answer("🎉 Tabriklaymiz, sizga sertifikat taqdim etildi!")

            filename = generate_filename(r['full_name'])  # ex: Ulugbek_Erkinov_sertifikat
            png_path = f"output/{filename}.png"
            pdf_url = f"https://qr.misterdev.uz/media/files/{filename}.pdf"

            # QR asosida sertifikat yaratish
            generated_path = generate_certificate(r['full_name'], r['overall'], png_path, pdf_url)
            if not generated_path:
                return await message.answer("❌ Sertifikat yaratishda xatolik.")

            # Yuklash
            upload_result = upload_certificate(png_path, filename)
            if upload_result:
                await message.answer_document(InputFile(upload_result["pdf_path"]))
                # await message.answer(f"📎 QR havola: {upload_result['qr_url']}")
            else:
                await message.answer("❌ Yuklashda xatolik.")

        # JSONdan o‘chirish