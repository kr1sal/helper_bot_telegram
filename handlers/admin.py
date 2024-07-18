from aiogram import Router

from middlewares import LanguageCheck

# Создаём роутер
router = Router()
router.message.middleware(LanguageCheck())
