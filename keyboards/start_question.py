from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="самолет")
    kb.button(text="поезд")
    kb.button(text="электричка")
    kb.button(text="автобус")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
