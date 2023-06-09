from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def chose_start_end() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Откуда")
    kb.button(text="Куда")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def chose_finish() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад")
    kb.button(text="Поиск")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def chose_hard_from() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Серп и молот")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def chose_hard_to() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Казанское")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def chose_station(stations) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for s, c in stations:
        kb.add(InlineKeyboardButton(text=c, callback_data=s))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
