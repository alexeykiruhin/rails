import asyncio
from aiogram import Bot, Dispatcher
from handlers import questions, start_end
import logging

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = '6178198572:AAGoZUXGvLrMey37QIASjnPFWLXPLrCEKLA'
API_KEY = 'bcbedf3a-ed56-419c-b2f6-0f6295f7cee5'


# Запуск бота
async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.include_routers(questions.router, start_end.router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
