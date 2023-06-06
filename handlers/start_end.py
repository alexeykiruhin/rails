from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def set_start_point(message: Message):
    print(f'message.text - {message.text}')
    await message.answer("Это текстовое сообщение!")

