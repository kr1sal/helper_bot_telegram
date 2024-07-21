import logging

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from services import Database

logger = logging.getLogger(__name__)

# Инициализируем router
router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, lang: str, lexicon: dict, db: Database):
    # Если пользователя нет в базе данных, то регистрируем его
    if not await db.get_user(message.from_user.id):
        await db.add_user(message.from_user.id)

        logger.info(f"New user (id: {message.from_user.id}) added to the database!")

    await message.answer(text=lexicon[lang]["commands"]["start"]["hello"])
