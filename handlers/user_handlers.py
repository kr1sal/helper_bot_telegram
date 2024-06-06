from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import language_kb
# from services.services import get_bot_choice, get_winner

from lexicon.lexicon_ru import COMMANDS, HELP, BASE

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=COMMANDS['start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text="\n\n".join(HELP.values()))


# Этот хэндлер срабатывает на команду /man
@router.message(Command(commands='man'))
async def process_man_command(message: Message):
    args = message.text.split()
    if len(args) == 1:
        answer = [HELP["man"]]
    else:
        answer = []
        for command in args[1:]:
            if command in HELP.keys():
                answer.append(HELP[command])
            else:
                answer.append("/" + command + " " + BASE["not_found"])

    await message.answer(text="\n\n".join(answer))


# Этот хэндлер срабатывает на команду /language
@router.message(Command(commands='language'))
async def process_help_command(message: Message):
    await message.answer(text=COMMANDS["language"],
                         reply_markup=language_kb)


# хендлер отвечает за CallbackQuery
@router.callback_query(F.data.in_(['ru_button_pressed',
                                   'en_button_pressed']))
async def process_buttons_press(callback: CallbackQuery):
    await callback.answer(text="Функция ещё не реализована")

# ...

