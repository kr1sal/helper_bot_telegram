import logging

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from filters import MessageData
from services import Database

logger = logging.getLogger(__name__)

# Инициализируем router
router = Router()


@router.message(CommandStart(), MessageData(), StateFilter(default_state))
async def process_start_command(message: Message, lang: str, lexicon: dict, db: Database):
    # Добавляем пользователя в базу данных и возвращаем результат в переменную
    added: bool = await db.add_user(message.from_user.id)
    # Если пользователь добавлен в базу данных, то информируем
    if added:
        logger.info(f"New user (id: {message.from_user.id}) added to the database!")

        # await message.answer(text=lexicon[lang]["commands"]["start"]["added"])

    await message.answer(text=lexicon[lang]["commands"]["start"]["hello"])
