from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reset_password = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Kodni qayta yuborish'),
        ],
    ],
    resize_keyboard=True
)

register = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧾Ro'yhatdan o'tish"),
        ],
    ],
    resize_keyboard=True
)

language = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿O'zbek tili"),
        ],
        [
            KeyboardButton(text="🇷🇺Русский язык")
        ]
    ],
    resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="ℹ️Shaxsiy ma'lumotlar"),
        ],
        [
            KeyboardButton(text="📚Ta'lim ma'lumotlari"),
        ],
        [
            KeyboardButton(text="📃Chet tili sertifikat qo'shish"),
        ],
        [
            KeyboardButton(text="🗂Yo'nalish tanlash"),
        ],
        [
            KeyboardButton(text="🈸Arizalar"),
        ]
        
    ],
    resize_keyboard=True
)

update_menu = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="📝Shaxsiy ma'lumotlarni tahrirlash"),
        ],
        [
            KeyboardButton(text="📖Ta'lim ma'lumotlarini tahrirlash"),
        ],
        [
            KeyboardButton(text="📃Chet tili sertifikatini tahrirlash"),
        ],
        [
            KeyboardButton(text="🈸Arizani tahrirlash"),
        ]
    ],
    resize_keyboard=True
)

application = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="🎓Daraja"),
        ],
        [
            KeyboardButton(text="🗂Yo'nalish yoki mutaxassislik"),
        ],
        [
            KeyboardButton(text="Ta'lim shakli"),
        ],
        [
            KeyboardButton(text="Ta'lim tili"),
        ]
    ],
    resize_keyboard=True
)
