import asyncio
from aiogram import Bot, Dispatcher
from handlers import questions, start_end
import logging
from settings import API_TOKEN

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


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
