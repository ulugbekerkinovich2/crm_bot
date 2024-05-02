from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_data import course_callback
from utils import send_req
# 1-usul
categoryMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='kurslar', callback_data='courses'),
            
        ],
        [
            InlineKeyboardButton(text='kitoblar', callback_data='books'),
        ]
        
    ]
)


#kurslar uchun keyboard
coursesMenu = InlineKeyboardMarkup(row_width=1)
course = InlineKeyboardButton(text="Foudation", callback_data=course_callback.new(item_name='kurs'))
coursesMenu.insert(course)

update_personal_info_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Familiya", callback_data='lastname'),
        ],
        [
            InlineKeyboardButton(text="Ism", callback_data='firstname'),
        ],
        [
            InlineKeyboardButton(text="Otangizni ismi", callback_data='thirdname'),
        ],
        [
            InlineKeyboardButton(text="Passport/ID karta seriya va raqami", callback_data='passport'),
        ],
        [
            InlineKeyboardButton(text="Tug'ilgan kun", callback_data='birthdate'),
        ],
        [
            InlineKeyboardButton(text="Jins", callback_data='gender'),
        ],
        [
            InlineKeyboardButton(text="Tug'ilgan joyi", callback_data='birthplace'),
        ],
        [
            InlineKeyboardButton(text="Qo'shimcha telefon raqami", callback_data='extra_phone'),
        ]
    ]
)


edit_user_education_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bitirgan yoki tahsil olayotgan ta'lim dargohi turi", callback_data='education'),
        ],
        [
            InlineKeyboardButton(text="Ta’lim dargohi joylashgan shahar yoki viloyat", callback_data='region'),
        ],
        [
            InlineKeyboardButton(text="Tumanni o'zgartirish", callback_data='district'),
        ],
        [
            InlineKeyboardButton(text="Ta'lim dargohi nomi", callback_data='education_name'),
        ],
        [
            InlineKeyboardButton(text="Diplom, shahodatnoma yoki ma’lumotnoma nusxasi", callback_data='diploma'),
        ],
        [
            InlineKeyboardButton(text="Chet tili sertifikati", callback_data='certificate'),
        ]
    ]
)

edit_user_education_transfer_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ta’lim dargohi joylashgan davlat", callback_data='country_id'),
        ],
        [
            InlineKeyboardButton(text="Ta'lim dargohi nomi", callback_data='institution_name'),
        ],
        [
            InlineKeyboardButton(text="Ta’lim yo’nalishi", callback_data='direction_name'),
        ],
        [
            InlineKeyboardButton(text="Ayni vaqtdagi kursingiz", callback_data='current_course'),
        ],
        [
            InlineKeyboardButton(text="Transkript nusxasi", callback_data='transcript'),
        ]
    ]
)
