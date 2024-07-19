from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config import config
from lexicon import LEXICON
from services import db


# Эти фильтры возвращают данные, необходимые для работы хендлеров
# Filter Message
class MessageData(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, Any]:
        # Формируем данные, которые содержат язык пользователя, лексикон и базу данных
        data = {}

        # Получить язык пользователя из базы данных
        lang: str = await db.get_language(message.from_user.id)

        # Если не получилось получить язык пользователя, то передаём язык по умолчанию
        if not (lang and lang in LEXICON.keys()):
            data["lang"] = config.default_language
        else:
            data["lang"] = lang

        # Передаём базу данных
        data["lexicon"] = LEXICON
        data["db"] = db

        return data


# Filter CallbackQuery
class CallbackQueryData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, Any]:
        # Формируем данные, которые содержат язык пользователя, лексикон и базу данных
        data = {}

        # Получить язык пользователя из базы данных
        lang: str = await db.get_language(callback.from_user.id)

        # Если не получилось получить язык пользователя, то передаём язык по умолчанию
        if not (lang and lang in LEXICON.keys()):
            data["lang"] = config.default_language
        else:
            data["lang"] = lang

        # Передаём базу данных
        data["lexicon"] = LEXICON
        data["db"] = db

        return data
