from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datetime import datetime


def date_picker() -> ReplyKeyboardMarkup:
    current_date = datetime.now()
    current_date_str = f'{current_date.year}-{current_date.month}-{current_date.day}'
    print(f'date picker')

    kb = ReplyKeyboardBuilder()
    kb.button(text="Дата")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)



