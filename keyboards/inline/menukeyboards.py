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