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
            KeyboardButton(text="🧾Abiturient"),
            KeyboardButton(text="🔄O'qishni ko'chirish"),
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
            KeyboardButton(text="ℹ️Shaxsiy ma'lumotlarim"),
            KeyboardButton(text="📚Ta'lim ma'lumotlarim"),
        ],
        # [
            # KeyboardButton(text="📃Chet tili sertifikat qo'shish"),
            # KeyboardButton(text="🗂Yo'nalish tanlash"),
        # ],
        [
            KeyboardButton(text="📁Arizam"),
#            KeyboardButton(text="🗑Akkauntni o'chirish"),
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
        # [
        #     KeyboardButton(text="📖Ta'lim ma'lumotlarini tahrirlash"),
        # ],
        # [
        #     KeyboardButton(text="📃Chet tili sertifikatini tahrirlash"),
        # ],
        # [
        #     KeyboardButton(text="🈸Arizani tahrirlash"),
        # ]
    ],
    resize_keyboard=True
)

update_personal_info = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="📝Shaxsiy ma'lumotlarni tahrirlash"),
        ],
        [
        KeyboardButton(text="📄Shaxsiy ma'lumotlarni ko'rish"),
        ]
    ],
    resize_keyboard=True
)

update_education_info = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="📝 Ta'lim ma'lumotlarni tahrirlash"),
        ],
        [
        KeyboardButton(text="📚 Ta'lim ma'lumotlarni ko'rish"),
        ]
    ],
    resize_keyboard=True
)

update_application = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="📝Arizani tahrirlash"),
        ],
        [
        KeyboardButton(text="📄Arizani ko'rish"),
        ]
    ]
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

finish_edit = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tahrirlashni yakunlash"),
        ]
    ],
    resize_keyboard=True
)


