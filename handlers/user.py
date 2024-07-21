from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from middlewares import RegisterCheck
from filters import MessageData, CallbackQueryData
from fsm import FSM
from keyboards import language_buttons, language_kb
from services import Database
from services import get_weather, get_http_in_cat, get_random_number, check_url, check_file_format, get_qr_code


# Инициализируем router и регистрируем middleware для незарегистрированных пользователей
router = Router()
router.message.middleware(RegisterCheck())


# Этот хендлер нужен, чтобы войти в состояние command_line, при котором доступны все команды
@router.message(Command(commands="cancel"), MessageData(), ~StateFilter(default_state))
async def process_cancel_command(message: Message, lang: str, lexicon: dict, state: FSMContext):
    await state.clear()

    await message.answer(text=lexicon[lang]["commands"]["cancel"])


# Этот хендлер нужен, чтобы удалить данные о пользователе из базы данных
@router.message(Command(commands="delete_all_data"), MessageData(), StateFilter(default_state))
async def process_delete_all_data(message: Message, lang: str, lexicon: dict, db: Database):
    await db.delete_user(message.from_user.id)

    await message.answer(text=lexicon[lang]["commands"]["delete_all_data"])


@router.message(Command(commands="help"), MessageData(), StateFilter(default_state))
async def process_help_command(message: Message, lang: str, lexicon: dict):
    answer: str = lexicon[lang]["help"].values()

    await message.answer(text="\n\n".join(answer))


@router.message(Command(commands="man"), MessageData(), StateFilter(default_state))
async def process_man_command(message: Message, lang: str, lexicon: dict):
    args: list[str] = message.text.split()

    if len(args) == 1:
        answer = [lexicon[lang]["help"]["man"]]
    else:
        answer = []
        for command in args[1:]:
            if command in lexicon[lang]["help"].keys():
                answer.append(lexicon[lang]["help"][command])
            else:
                answer.append("/" + command + " - " + lexicon[lang]["errors"]["not_found"])

    await message.answer(text="\n\n".join(answer))


@router.message(Command(commands="language"), MessageData(), StateFilter(default_state))
async def process_language_command(message: Message, lang: str, lexicon: dict, state: FSMContext):
    args: list[str] = message.text.split()

    match len(args):
        # Если указана только команда /language, то вызываем сообщение с кнопками
        case 1:
            await message.answer(text=lexicon[lang]["commands"]["language"]["select"],
                                 reply_markup=language_kb)

        # Если указана команда /language change
        case 2:
            if args[1].lower() == "change":
                # Превращаем словарь в одномерный список, чтобы вывести его сообщением
                langs: list[str] = []
                for key, value in lexicon.items():
                    langs.append(key)
                    langs.append(value["name"])
                # Устанавливаем состояние, передаём языки в data и отвечаем сообщением
                await state.set_data({"langs": langs})
                await state.set_state(FSM.change_language_state)
                await message.answer(text=lexicon[lang]["commands"]["language"]["enter"].format(langs=", ".join(langs)))

            else:
                await message.answer(text=lexicon[lang]["errors"]["invalid"])

        # Иначе выводим "неверный синтаксис"
        case _:
            await message.answer(text=lexicon[lang]["errors"]["wrong_args"])


""" Language """


@router.message(MessageData(), StateFilter(FSM.change_language_state))
async def process_change_language(message: Message, lang: str, lexicon: dict, db: Database, state: FSMContext):
    args: list[str] = message.text.split()

    langs: list[str] = (await state.get_data())["langs"]
    # Считаем чётный индекс id, а нечётный name
    for i in range(0, len(langs), 2):
        lang_id: str = langs[i].lower()
        lang_name: str = langs[i+1].lower()
        # Перебираем все аргументы и ищем доступные языки
        for arg in args:
            arg = arg.lower()
            if arg in lang_id or arg in lang_name:
                # Используем id языков, чтобы получить соответствующие языковые ресурсы (keys for lexicon)
                lang = lang_id
                lang_old = await db.get_language(message.from_user.id)
                await db.set_language(message.from_user.id, lang)

                answer = lexicon[lang]["commands"]["language"]["change"].format(
                    language_old=lexicon[lang_old]["name"], language=lexicon[lang]["name"])
                await state.clear()
                return await message.answer(text=answer)

    # Иначе выводим сообщение о доступных языках
    else:
        await message.answer(text=lexicon[lang]["commands"]["language"]["enter"].format(langs=", ".join(langs)))


@router.callback_query(F.data.in_([lang_button.callback_data for lang_button in language_buttons]), CallbackQueryData(), StateFilter(default_state))
async def change_language(callback: CallbackQuery, lexicon: dict, db: Database):
    # Получаем язык, на который хотим поменять текущий
    lang = callback.data.title().upper()[:2]
    lang = lang.lower()

    # Меняем язык на lang и получаем прошлый, на котором разговаривал бот
    lang_old = await db.get_language(callback.from_user.id)
    await db.set_language(callback.from_user.id, lang)

    answer = lexicon[lang]["commands"]["language"]["change"].format(
        language_old=lexicon[lang_old]["name"], language=lexicon[lang]["name"])

    await callback.answer(text=answer)


""" Weather """


@router.message(Command(commands='weather'), MessageData(), StateFilter(default_state))
async def process_weather_command(message: Message, lang: str, lexicon: dict, state: FSMContext):
    args = message.text.split()

    match len(args):
        # Если указана только команда, то переходим в состояние get_city
        case 1:
            await state.set_state(FSM.get_city_state)
            await message.answer(text=lexicon[lang]["commands"]["weather"]["enter_city"])

        # Иначе выводим
        case _:
            await message.answer(text=lexicon[lang]["errors"]["wrong_args"])


@router.message(MessageData(), StateFilter(FSM.get_city_state))
async def process_get_city(message: Message, lang: str, lexicon: dict, state: FSMContext):
    answer = get_weather(message.text, lang.upper())
    # Если ответ не пустой, то обрабатываем его
    if answer:
        await state.clear()
        await message.answer(text="\n".join((
            lexicon[lang]["commands"]["weather"]["main"].format(city=answer[0]),
            lexicon[lang]["commands"]["weather"]["description"].format(description=answer[1]),
            lexicon[lang]["commands"]["weather"]["temperature"].format(temperature=answer[2]),
            lexicon[lang]["commands"]["weather"]["wind_speed"].format(wind_speed=answer[3])
        )))
    # Иначе выводит - город не найден
    else:
        await message.answer(text=lexicon[lang]["errors"]["city_not_found"].format(city=message.text))


@router.message(Command(commands='http_in_cat'), MessageData(), StateFilter(default_state))
async def process_http_in_cat_command(message: Message, lang: str, lexicon: dict):
    args = message.text.split()

    match len(args):
        # Если указана только команда, то переходим в состояние get_city
        case 1:
            await message.answer_photo(get_http_in_cat())

        # если указан аргумент, считаем его кодом HTTP
        case 2:
            try:
                code: int = int(args[1])
            except TypeError:
                return await message.answer(text=lexicon[lang]["errors"]["invalid"])

            photo = get_http_in_cat(code)
            if not photo:
                return await message.answer(text=lexicon[lang]["errors"]["http_not_found"].format(code=code))

            await message.answer_photo(photo)

        # Иначе выводим инвалид синтаксис
        case _:
            await message.answer(text=lexicon[lang]["errors"]["wrong_args"])


@router.message(Command(commands='random'), MessageData(), StateFilter(default_state))
async def process_random_command(message: Message, lang: str, lexicon: dict):
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
                await message.answer(text=lexicon[lang]["errors"]["invalid"])

        # Если введена команда с аргументами start и end, то возвращаем рандомное число от start до end
        case 3:
            try:
                await message.answer(text=str(get_random_number(int(args[1]), int(args[2]))))
            except TypeError:
                await message.answer(text=lexicon[lang]["errors"]["invalid"])

        # Иначе выводим - инвалид
        case _:
            await message.answer(text=lexicon[lang]["errors"]["wrong_args"])


@router.message(Command(commands='qr_code'), MessageData(), StateFilter(default_state))
async def process_qr_code_command(message: Message, lang: str, lexicon: dict, state: FSMContext):
    args = message.text.split()

    match len(args):
        case 1:
            await state.set_state(FSM.get_qr_code_state)
            await message.answer(text=lexicon[lang]["commands"]["qr_code"])

        # иначе выводим инвалида
        case _:
            await message.answer(text=lexicon[lang]["errors"]["wrong_args"])


@router.message(MessageData(), StateFilter(FSM.get_qr_code_state))
async def process_get_qr_code(message: Message, lang: str, lexicon: dict, state: FSMContext):
    args = message.text.split()

    match len(args):
        case 1:
            url = args[0]
            if not check_url(url):
                return await message.answer(text=lexicon[lang]["errors"]["wrong_url"])

            await state.clear()
            await message.answer_photo(photo=get_qr_code(url))

        case 3:
            url: str = args[0]
            if not check_url(url):
                return await message.answer(text=lexicon[lang]["errors"]["wrong_url"])

            try:
                size: int = int(args[1])
            except ValueError:
                return await message.answer(text=lexicon[lang]["errors"]["wrong_size"])

            file_format: str = args[2]
            if not check_file_format(args[2]):
                return await message.answer(text=lexicon[lang]["errors"]["wrong_file_format"])

            await state.clear()
            await message.answer_document(document=get_qr_code(url, size, file_format))

        case _:
            await message.answer(text=lexicon[lang]["errors"]["wrong_args"])


"""
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
"""


# Этот хендлер отвечает, если были проигнорированы другие хендлеры
@router.message(MessageData(), StateFilter(default_state))
async def process_other_command(message: Message, lang: str, lexicon: dict):
    await message.answer(text=lexicon[lang]["commands"]["other"])
