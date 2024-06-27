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

register_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧾 Абитуриент"),
            KeyboardButton(text="🔄Трансферное обучение"),
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

menu_full = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="ℹ️Shaxsiy ma'lumotlarim"),
            KeyboardButton(text="📚Ta'lim ma'lumotlarim"),
        ],
        [
            KeyboardButton(text="📁Arizam"),
           KeyboardButton(text="📃Imtihon natijalari"),
        ],
        [
            KeyboardButton(text="Akkauntdan chiqish"),
        ]
    ],
    resize_keyboard=True
)
menu_ru = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="ℹ️Моя личная информация"),
            KeyboardButton(text="📚Моя образовательная информация"),
        ],
        [
            KeyboardButton(text="📁Заявление"),
#            KeyboardButton(text="🗑Akkauntni o'chirish"),
        ],
        [
            KeyboardButton(text="Выйти из аккаунта"),
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
update_menu_ru = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="📝 Редактировать личную информацию"),
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

update_personal_info_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="📝 Редактировать личную информацию"),
        ],
        [
        KeyboardButton(text="📄Просмотр личной информации"),
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
update_education_info_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="📝 Редактировать образовательную информацию"),
        ],
        [
        KeyboardButton(text="📚 Просмотр образовательной информации"),
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
update_application_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="📝Редактировать заявление"),
        ],
        [
        KeyboardButton(text="📄 Посмотреть заявление"),
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
application_ru = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="🎓 Степень"),
        ],
        [
            KeyboardButton(text="🗂 Направление или специальность"),
        ],
        [
            KeyboardButton(text="Форма обучения"),
        ],
        [
            KeyboardButton(text="Язык обучения"),
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
enter_button_ru = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='Продолжить'),
        ]
    ],
    resize_keyboard=True
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ha, mavjud'),
             KeyboardButton(text="Yo'q, mavjud emas"),
        ],
        [
            KeyboardButton(text="Bekor qilish"),
        ]
    ],
    resize_keyboard=True
)
yes_no_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да, есть'),
            KeyboardButton(text="Нет, не доступен")
        ],
        [
            KeyboardButton(text="Отмена"),
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
ask_delete_account_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да, удалить аккаунт"),
            KeyboardButton(text="Отмена"),
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
exit_from_account_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да, выйти"),
            KeyboardButton(text="Отмена"),
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

finish_edit_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Завершить редактирование"),
        ]
    ],
    resize_keyboard=True
)


