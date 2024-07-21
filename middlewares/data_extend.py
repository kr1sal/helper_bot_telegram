from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from config import config
from services import db
from lexicon import LEXICON


class DataExtend(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        # Получить язык пользователя из базы данных
        lang: str = await db.get_language(event.from_user.id)

        # Если не получилось получить язык пользователя, то передаём язык по умолчанию
        if not (lang and lang in LEXICON.keys()):
            data["lang"] = config.default_language
        else:
            data["lang"] = lang

        # Передаём базу данных
        data["lexicon"] = LEXICON
        data["db"] = db

        return await handler(event, data)
