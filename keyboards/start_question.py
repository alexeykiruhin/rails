from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


transport = ['самолет', 'поезд', 'электричка', 'автобус']


def start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for t in transport:
        kb.button(text=t)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
