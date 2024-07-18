from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from services import db
from lexicon.lexicon import LEXICON

# Инициализируем router
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    # Добавляем пользователя в базу данных
    await db.add_user(message.from_user.id)
    # Получаем язык коммуникации, по умолчанию английский en
    lang = await db.get_language(message.from_user.id)
    # Достаём ответ из словаря лексикона
    answer = LEXICON[lang]["commands"]["start"]

    await message.answer(text=answer)
