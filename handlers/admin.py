from aiogram import Router

from middlewares import RegisterCheck

# Создаём роутер
router = Router()
router.message.middleware(RegisterCheck())
