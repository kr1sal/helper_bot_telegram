from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from config import config
from services import db
from lexicon import LEXICON


class LanguageCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Если пользователя нет в базе данных, то возвращаем сообщение с ошибкой
        if not await db.get_user(event.from_user.id):
            await event.answer(LEXICON[config.default_language]["errors"]["not_registered"])
            return

        return await handler(event, data)
