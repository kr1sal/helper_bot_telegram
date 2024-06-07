from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import language_kb
from services.services import get_weather, get_random_http, check_http,  get_http_in_cat, get_random_number

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
async def process_language_command(message: Message):
    await message.answer(text=COMMANDS["language"],
                         reply_markup=language_kb)


# хендлер отвечает за CallbackQuery
@router.callback_query(F.data.in_(['ru_button_pressed',
                                   'en_button_pressed']))
async def process_buttons_press(callback: CallbackQuery):
    await callback.answer(text="Функция ещё не реализована")


# Этот хэндлер срабатывает на команду /weather
@router.message(Command(commands='weather'))
async def process_weather_command(message: Message):
    args = message.text.split()
    if len(args) == 1:
        answer = get_weather("12323")
    elif len(args) == 2:
        answer = get_weather(message[1])
    else:
        answer = BASE["invalid"]

    await message.answer(text=answer)


# Этот хэндлер срабатывает на команду /http_in_cat
@router.message(Command(commands='http_in_cat'))
async def process_http_in_cat_command(message: Message):
    args = message.text.split()
    # При одном аргументе бот отвечает рандомной картинкой
    if len(args) == 1:
        await message.answer_photo(photo=get_http_in_cat(get_random_http()))
    # При двух определённый код, переданный вторым аргументом
    elif len(args) == 2:
        try:
            if check_http(int(args[1])):
                await message.answer_photo(photo=get_http_in_cat(int(args[1])))
            else:
                await message.answer(text=get_http_in_cat(int(args[1])))

        except TypeError:
            await message.answer(text=BASE["invalid"])
    # Иначе выводит инвалида
    else:
        await message.answer(text=BASE["invalid"])


# Этот хэндлер срабатывает на команду /random
@router.message(Command(commands='random'))
async def process_random_command(message: Message):
    args = message.text.split()
    if len(args) == 1:
        answer = get_random_number()

    elif len(args) > 3:
        answer = BASE["invalid"]

    else:
        try:
            if len(args) == 2:
                answer = get_random_number(0, int(args[1]))
            else:
                answer = get_random_number(int(args[1]), int(args[2]))

        except TypeError:
            answer = BASE["invalid"]

    await message.answer(text=str(answer))
