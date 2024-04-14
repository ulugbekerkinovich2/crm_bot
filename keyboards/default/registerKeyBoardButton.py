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
            KeyboardButton(text="📚Ta'lim ma'lumotlari"),
        ],
        [
            KeyboardButton(text="📃Chet tili sertifikat qo'shish"),
            KeyboardButton(text="🗂Yo'nalish tanlash"),
        ],
        [
            KeyboardButton(text="🈸Arizalar"),
            KeyboardButton(text="🗑Akkauntni o'chirish"),
        ],
        [
            KeyboardButton(text="Akkauntdan chiqish"),
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

enter_button = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='Davom etish'),
        ]
    ],
    resize_keyboard=True
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ha, mavjud'),
        ],
        [
            KeyboardButton(text="Yo'q, mavjud emas"),
        ]
    ],
    resize_keyboard=True
)

ask_delete_account = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha, akkauntni o'chirish"),
            KeyboardButton(text="Bekor qilish"),
        ]
    ],
    resize_keyboard=True
)

exit_from_account = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha, Akkauntdan chiqish"),
            KeyboardButton(text="Bekor qilish"),
        ]
    ],
    resize_keyboard=True
)