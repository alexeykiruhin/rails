from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def chose_date() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Сегодня")
    kb.button(text="Другая дата")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
