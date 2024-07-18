import datetime as dt

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from middlewares import LanguageCheck
from keyboards import language_buttons, language_kb, birthdays_kb
from services import *
from services import db
from lexicon.lexicon import LEXICON


# Инициализируем router и регистрируем middleware для незарегистрированных пользователей
router = Router()
router.message.middleware(LanguageCheck())


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    lang = await db.get_language(message.from_user.id)

    answer = LEXICON[lang]["help"].values()

    await message.answer(text="\n\n".join(answer))


@router.message(Command(commands='man'))
async def process_man_command(message: Message):
    lang = await db.get_language(message.from_user.id)

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


@router.message(Command(commands='language'))
async def process_language_command(message: Message):
    lang = await db.get_language(message.from_user.id)

    args = message.text.split()
    match len(args):
        case 1:
            await message.answer(text=LEXICON[lang]["COMMANDS"]["language"],
                                 reply_markup=language_kb)

        case 3:
            if args[1].lower() == "change":
                languages = []
                for key in LEXICON.keys():
                    languages.extend([key, LEXICON[key]["name"].upper()])

                query = args[2].upper()
                for i in range(0, len(languages), 2):
                    if query == languages[i] or query == languages[i+1]:
                        # Меняем язык на запрашиваемый и выводим ответ
                        lang, lang_old = languages[i], lang
                        await db.change_language(message.from_user.id, lang)
                        answer = LEXICON[lang]["COMMANDS"]["change_language"].format(language_old=lang_old,
                                                                                     language=lang)
                        await message.answer(text=answer)
                        break
                else:
                    await message.answer(text="language not found")
            else:
                await message.answer(text=LEXICON[lang]["BASE"]["invalid"])

        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])


@router.message(Command(commands='weather'))
async def process_weather_command(message: Message):
    lang = await db.get_language(message.from_user.id)

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
                    LEXICON[lang]["COMMANDS"]["weather"]["main"].format(city=answer[0]),
                    LEXICON[lang]["COMMANDS"]["weather"]["description"].format(description=answer[1]),
                    LEXICON[lang]["COMMANDS"]["weather"]["temperature"].format(temperature=answer[2]),
                    LEXICON[lang]["COMMANDS"]["weather"]["wind_speed"].format(wind_speed=answer[3])
                ))
            else:
                answer = LEXICON[lang]["COMMANDS"]["city_not_found"]

            await message.answer(text=answer)

        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])


@router.message(Command(commands='http_in_cat'))
async def process_http_in_cat_command(message: Message):
    lang = await db.get_language(message.from_user.id)

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
                    await message.answer(text=LEXICON[lang]["COMMANDS"]["http_404"])

            except TypeError:
                await message.answer(text=LEXICON[lang]["BASE"]["invalid"])

        # Иначе выводит - инвалид
        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])


@router.message(Command(commands='random'))
async def process_random_command(message: Message):
    lang = await db.get_language(message.from_user.id)

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


@router.message(Command(commands='qr_code'))
async def process_qr_code_command(message: Message):
    lang = await db.get_language(message.from_user.id)

    args = message.text.split()
    match len(args):
        # Если введена только команда, то выводит справку
        case 1:
            await message.answer(text=LEXICON[lang]["HELP"]["qr_code"])

        # Если есть второй аргумент, считаем его ссылкой и обрабатываем ошибки
        case 2:
            answer = get_qr_code(args[1])
            if type(answer) is URLInputFile:
                await message.answer_photo(photo=answer)
            elif answer == 1:
                await message.answer(text=LEXICON[lang]["COMMANDS"]["wrong_url"])
            elif answer == 2:
                await message.answer(text=LEXICON[lang]["COMMANDS"]["wrong_file_format"])
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


@router.message(Command(commands='birthdays'))
async def process_birthdays_command(message: Message):
    lang = await db.get_language(message.from_user.id)

    # Если сообщение слишком длинное, то отвечаем исключением
    if len(message.text) >= 100:
        await message.answer(text=LEXICON[lang]["BASE"]["long_message"])
        return

    # Получаем аргументы и список дней рождений пользователя
    args = get_args(message.text)
    birthdays = await db.get_user_birthdays(message.from_user.id)

    # Если передана только команда, то возвращаем меню birthdays
    if len(args) == 1:
        if birthdays:
            answer = []
            counter = 1
            for birthday_id, user_id, name, date, years in birthdays:
                delimiter = " " * (8 - len(str(counter)) * 2)
                answer.append(LEXICON[lang]["COMMANDS"]["birthdays"]["birthday"].format(id=counter, name=name, date=date, years=years, delimiter=delimiter))
                counter += 1

            await message.answer(text="\n".join(answer),
                                 reply_markup=birthdays_kb)

        else:
            await message.answer(text=LEXICON[lang]["COMMANDS"]["birthdays"]["404"],
                                 reply_markup=birthdays_kb)

        return

    # Иначе работаем в режиме командной строки
    match args[1].lower():
        # Если первый аргумент list, то выводим список дней рождений
        case "list":
            # Если дни рождения существуют в базе данных, то форматируем и выводим
            if birthdays:
                answer = []
                counter = 1
                for birthday_id, user_id, name, date, years in birthdays:
                    delimiter = " " * (8 - len(str(counter))*2)
                    answer.append(LEXICON[lang]["COMMANDS"]["birthdays"]["birthday"].format(id=counter, name=name, date=date, years=years, delimiter=delimiter))
                    counter += 1

                await message.answer(text="\n".join(answer))

            # Иначе выводим 404
            else:
                await message.answer(text=LEXICON[lang]["COMMANDS"]["birthdays"]["404"])

        # Если первый аргумент add, то добавляем новый день рождения
        case "add":
            # Если достигнуто максимум дней рождений в базе данных, то отвечаем исключением
            if len(birthdays) >= 100:
                await message.answer(text="many_birthdays")
                return

            if len(args) == 5:
                name = args[2]
                year, month, day = map(int, multi_split(["-", "."], args[3]))
                date = dt.date(year, month, day)
                years = int(args[4])
                await db.add_birthday(message.from_user.id, name, date, years)
                # scheduler.add_job()

            else:
                await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])

        # Если первый аргумент change, то изменяем данные о дне рождения
        case "change":
            if len(args) == 5:
                index = int(args[2])

                match args[3].lower():
                    case "name":
                        name = args[4]
                        await db.change_name_birthday(birthdays[index-1][0], name)

                    case "date":
                        year, month, day = map(int, multi_split(["-", "."], args[3]))
                        date = dt.date(year, month, day)
                        await db.change_date_birthday(birthdays[index-1][0], date)

                    case "years":
                        years = int(args[4])
                        await db.change_years_birthday(birthdays[index-1][0], years)

                    case _:
                        await message.answer(text=LEXICON[lang]["BASE"]["invalid"])

            else:
                await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])

        # Если первый аргумент delete, то удаляем день рождения
        case "delete":
            if len(args) >= 3:
                index = int(args[2])

                if index in range(1, len(birthdays)+1):
                    await db.delete_birthday(birthdays[index-1][0])
                else:
                    await message.answer(text=LEXICON[lang]["COMMANDS"]["birthdays"]["out_of_range"])

            else:
                await message.answer(text=LEXICON[lang]["BASE"]["wrong_args"])

        # Иначе выводим инвалид
        case _:
            await message.answer(text=LEXICON[lang]["BASE"]["invalid"])


""" CALLBACK QUERY """


@router.callback_query(F.data.in_([lang_button.callback_data for lang_button in language_buttons]))
async def process_buttons_press(callback: CallbackQuery):
    # Получаем язык, на который хотим поменять текущий
    lang = callback.data.title().upper()[:2]

    # Меняем язык на lang и получаем прошлый, на котором разговаривал бот
    lang_old = await db.change_language(callback.from_user.id, lang)

    answer = LEXICON[lang]["COMMANDS"]["change_language"].format(language_old=lang_old, language=lang)

    await callback.answer(text=answer)
