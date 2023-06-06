from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datetime import datetime


def chose_date() -> ReplyKeyboardMarkup:
    current_date = datetime.now()
    current_date_str = f'{current_date.year}-{current_date.month}-{current_date.day}'
    print(current_date_str)

    kb = ReplyKeyboardBuilder()
    kb.button(text="сегодня")
    kb.button(text="другая дата")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
