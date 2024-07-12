from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.keyboards import language_kb
from services.services import get_weather, get_random_http, check_http,  get_http_in_cat, get_random_number, get_qr_code, get_type_of_urlinputfile
from services.db_services import Database
from lexicon.lexicon import LEXICON

# Создаём роутер и базу данных
router = Router()
db = Database()


""" SERVICE HANDLERS """


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    # Добавляем пользователя в базу данных
    db.add_user(message.from_user.id)
    # Получаем язык коммуникации, по умолчанию английский EN
    lang = db.get_language(message.from_user.id)
    # Достаём ответ из словаря лексикона
    answer = LEXICON[lang]["COMMANDS"]["start"]

    await message.answer(text=answer)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    lang = db.get_language(message.from_user.id)

    answer = LEXICON[lang]["HELP"].values()

    await message.answer(text="\n\n".join(answer))


# Этот хэндлер срабатывает на команду /man
@router.message(Command(commands='man'))
async def process_man_command(message: Message):
    lang = db.get_language(message.from_user.id)

    # Получаем аргументы и считываем команды
    args = message.text.split()
    if len(args) == 1:
        answer = [LEXICON[lang]["HELP"]["man"]]
    else:
        answer = []
        for command in args[1:]:
            if command in LEXICON[lang]["HELP"].keys():
                answer.append(LEXICON[lang]["HELP"][command])
            else:
                answer.append("/" + command + " " + LEXICON[lang]["BASE"]["not_found"])

    await message.answer(text="\n\n".join(answer))


# Этот хэндлер срабатывает на команду /language
@router.message(Command(commands='language'))
async def process_language_command(message: Message):
    lang = db.get_language(message.from_user.id)

    answer = LEXICON[lang]["COMMANDS"]["language"]

    await message.answer(text=answer,
                         reply_markup=language_kb)


# Этот хэндлер срабатывает на команду /weather
@router.message(Command(commands='weather'))
async def process_weather_command(message: Message):
    lang = db.get_language(message.from_user.id)

    args = message.text.split()
    match len(args):
        # Если указана только команда - выводим справку
        case 1:
            await message.answer(text=LEXICON[lang]["HELP"]["weather"])

        # При указании 1 аргумента, считаем его городом и обрабатываем
        case 2:
            answer = get_weather(args[1], lang)
            if answer:
                answer = "\n".join((
                    LEXICON[lang]["SERVICES"]["weather"]["main"].format(city=answer[0]),
                    LEXICON[lang]["SERVICES"]["weather"]["description"].format(description=answer[1]),
                    LEXICON[lang]["SERVICES"]["weather"]["temperature"].format(temperature=answer[2]),
                    LEXICON[lang]["SERVICES"]["weather"]["wind_speed"].format(wind_speed=answer[3])
                ))
            else:
                answer = LEXICON[lang]["SERVICES"]["city_not_found"]

            await message.answer(text=answer)

        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])


# Этот хэндлер срабатывает на команду /http_in_cat
@router.message(Command(commands='http_in_cat'))
async def process_http_in_cat_command(message: Message):
    lang = db.get_language(message.from_user.id)

    args = message.text.split()
    match len(args):
        # При одном аргументе бот отвечает рандомной картинкой
        case 1:
            await message.answer_photo(photo=get_http_in_cat(get_random_http()))

        # При двух определённый код, переданный вторым аргументом
        case 2:
            try:
                if check_http(int(args[1])):
                    await message.answer_photo(photo=get_http_in_cat(int(args[1])))
                else:
                    await message.answer(text=LEXICON[lang]["SERVICES"]["404"])

            except TypeError:
                await message.answer(text=LEXICON[lang]["BASE"]["invalid"])

        # Иначе выводит - инвалид
        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])


# Этот хэндлер срабатывает на команду /random
@router.message(Command(commands='random'))
async def process_random_command(message: Message):
    lang = db.get_language(message.from_user.id)

    args = message.text.split()
    match len(args):
        # Если введена только команда, то возвращаем рандомное число от 0 до 100
        case 1:
            await message.answer(text=str(get_random_number()))

        # Если введена команда с одним аргументом end, то возвращаем рандомное число от 0 до end
        case 2:
            try:
                await message.answer(text=str(get_random_number(0, int(args[1]))))
            except TypeError:
                await message.answer(text=LEXICON[lang]["BASE"]["invalid"])

        # Если введена команда с аргументами start и end, то возвращаем рандомное число от start до end
        case 3:
            try:
                await message.answer(text=str(get_random_number(int(args[1]), int(args[2]))))
            except TypeError:
                await message.answer(text=LEXICON[lang]["BASE"]["invalid"])

        # Иначе выводим - инвалид
        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])


# Этот хэндлер срабатывает на команду /qr_code
@router.message(Command(commands='qr_code'))
async def process_random_command(message: Message):
    lang = db.get_language(message.from_user.id)

    args = message.text.split()
    match len(args):
        # Если введена только команда, то выводит справку
        case 1:
            await message.answer(text=LEXICON[lang]["HELP"]["qr_code"])

        # Если есть второй аргумент, считаем его ссылкой и обрабатываем ошибки
        case 2:
            answer = get_qr_code(args[1])
            if type(answer) is get_type_of_urlinputfile():
                await message.answer_photo(photo=answer)
            elif answer == 1:
                await message.answer(text=LEXICON[lang]["SERVICES"]["wrong_url"])
            elif answer == 2:
                await message.answer(text=LEXICON[lang]["SERVICES"]["wrong_file_format"])
            else:
                await message.answer(text=LEXICON[lang]["BASE"]["invalid"])

        # Не работает
        case 5:
            await message.answer(text=LEXICON[lang]["BASE"]["tech_work"])
            """
            try:
                if args[4].lower() == "true":
                    answer = get_qr_code(url=args[1], size=int(args[2]), file_format=args[3], transparent=True)
                else:
                    answer = get_qr_code(args[1], int(args[2]), args[3])
    
                if type(answer) is get_type_of_urlinputfile():
                    await message.answer_photo(photo=answer)
                else:
                    await message.answer(text=answer)
            except TypeError:
                await message.answer(text=BASE["invalid"])
            """

        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])


""" CALLBACK QUERY """


# хендлер отвечает за CallbackQuery en_button_pressed
@router.callback_query(F.data.in_(['en_button_pressed']))
async def process_buttons_press(callback: CallbackQuery):
    lang = "EN"

    # Меняем язык на английский
    lang_old = db.change_language(callback.from_user.id, lang)

    answer = LEXICON[lang]["SERVICES"]["change_language"].format(language_old=lang_old, language=lang)

    await callback.answer(text=answer)


# хендлер отвечает за CallbackQuery ru_button_pressed
@router.callback_query(F.data.in_(['ru_button_pressed']))
async def process_buttons_press(callback: CallbackQuery):
    lang = "RU"

    # Меняем язык на русский
    lang_old = db.change_language(callback.from_user.id, lang)

    answer = LEXICON[lang]["SERVICES"]["change_language"].format(language_old=lang_old, language=lang)

    await callback.answer(text=answer)


""" OTHER HANDLERS """


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    lang = db.get_language(message.from_user.id)

    answer = LEXICON[lang]["BASE"]["other_answer"]

    await message.answer(text=answer)
