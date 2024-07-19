import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import start_router, user_router, admin_router

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s #%(levelname)-8s [%(filename)s] - %(name)s - %(message)s")

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage = MemoryStorage()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.bot_token,
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=storage)

    # Регистрируем роутеры в диспетчере
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Пропускаем накопившиеся updates и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
