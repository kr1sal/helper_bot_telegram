import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import config
from handlers import start_router, user_router, admin_router
from services import db
from lexicon import LEXICON

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.bot_token,
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    # Регистрируем роутеры в диспетчере
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Пропускаем накопившиеся updates и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
