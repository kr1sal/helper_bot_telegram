from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon_ru import BASE

router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    await message.answer(text=BASE['other_answer'])
