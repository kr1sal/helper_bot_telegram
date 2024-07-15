LEXICON: dict = {
    # Русский
    "RU": {
        "name": "Русский",

        "BASE": {
            "other_answer": "Увы, это сообщение мне непонятно...",
            "not_found": "Команда не найдена!",
            "invalid": "Неправильный синтаксис команды!",
            "wrong_args": "Неверное количество переданных аргументов!",
            "long_message": "Слишком длинное сообщение!",
            "tech_work": "Технические шоколадки!",
        },

        "COMMANDS": {
            "start": "<b>Привет!\n"
                     "Я виртуальный помощник</b>\n\n"
                     "Чтобы получить список команд введите /help\n\n"
                     "Для смены языка введите /language",
            "man": "Справка: [аргумент] {множество аргументов} [*аргумент], где *необязательный.",
            "language": "Выберите язык!",
            "change_language": "Вы сменили язык: {language_old} ==> {language}.",
            "weather": {
                "main": "Погода в <b>{city}</b> сейчас такая:",
                "description": "За окном: <b>{description}</b>",
                "temperature": "Температура: <b>{temperature}°C</b>",
                "wind_speed": "Скорость ветра: <b>{wind_speed}</b> м/с",
            },
            "city_not_found": "Невозможно определить погоду для <b>{city}</b>.",
            "http_404": "Ошибка 404! Код HTTP не найден!",
            "qr_code": {
                "wrong_url": "Указан неверный url. Перепроверьте ссылку!",
                "wrong_file_format": "Неверный формат файла {format_file}!",
            },
            "birthdays": {
                "birthday": "№{id}{delimiter}У {name} ({years}) в {date} ДР!",
                "404": "Дни рождения не обнаружены!",
                "out_of_range": "Дня рождения с таким номером не обнаружено!",
                "many_birthdays": "Слишком много дней рождений! Моя база данных не справиться с большим кол-вом!",
            },
        },

        "HELP": {
            "start": "<b>/start</b> - <i>Вывести приветственное сообщение.</i>",
            "help": "<b>/help</b> - <i>Вывести список команд.</i>",
            'man': '<b>/man {commands}</b> - <i>Вывести документацию отдельно для каждой команды. Пишите команды без слеша.</i>',
            "language": "<b>/language</b> - <i>Выбрать язык коммуникации.</i>",
            "weather": "<b>/weather [city]</b> - <i>Вывести прогноз погоды на сегодня в городе city.</i>",
            "http_in_cat": "<b>/http_in_cat [*code]</b> - <i>Вывести случайную картинку с кодом http или с переданным code.</i>",
            "random": "<b>/random [*end] | /random [*start] [*end]</b> - <i>Выводит рандомное число от 0 до 100, если не переданы аргументы. \n"
                      "Выводит от 0 до end или от start до end.</i>",
            "qr_code": "<b>/qr_code [url] [*size] [*format] [*transparent]</b> - <i>Возвращает изображение QR-кода на url, размером size, форматом format (png | svg) и прозрачностью (true false). \n"
                       "Указывайте либо 1 аргумент, либо 4 аргумента.</i>",
            "birthdays": "<b>/birthdays</b> - <i>Команда выводит меню с кнопками для взаимодействия со днями рождениями.\n</i>"
                         "<b>/birthdays list</b> - <i>Выводит список дней рождений.\n</i>" 
                         "<b>/birthdays add [name] [date] [years]</b> - <i>Добавляем новую запись с данными о дне рождении. "
                         "Имя человека (или иное существо) name, датой date, возрастом years.\n</i>"
                         "<b>/birthdays change [id] [name|date|years] [arg]</b> - <i>Меняет одно значение (name | date | years) записи номера id arg. "
                         "Чтобы указать имя, состоящее более, чем из одного слова, необходимо обособить кавычками \" или \'.</i>",
        },
    },

    # English, just English
    "EN": {
        "name": "English",

        "BASE": {
            "other_answer": "Unfortunately, this message is not clear to me...",
            "not_found": "Command not found!",
            "invalid": "Invalid command syntax!",
            "wrong_args": "Wrong number of arguments passed!",
            "long_message": "Message too long!",
            "tech_work": "Technical chocolates!",
        },

        "COMMANDS": {
            "start": "<b>Hello!\n"
                     "I'm a virtual assistant</b>\n\n"
                     "To get a list of commands, type /help\n\n"
                     "To change the language, enter /language",
            "man": "Help: [argument] {set of arguments} [*argument], where *optional.",
            "language": "Choose a language!",
            "change_language": "You have changed the language: {language_old} ==> {language}.",
            "weather": {
                "main": "The current weather in <b>{city}</b> is:",
                "description": "Outside the window: <b>{description}</b>",
                "temperature": "Temperature: <b>{temperature}°C</b>",
                "wind_speed": "Wind speed: <b>{wind_speed}</b> m/s",
            },
            "city_not_found": "Unable to determine the weather for <b>{city}</b>.",
            "http_404": "Error 404! HTTP code not found!",
            "qr_code": {
                "wrong_url": "Invalid url. Please double check the link!",
                "wrong_file_format": "Wrong file format {format_file}!",
            },
            "birthdays": {
                "birthday": "No.{id}{delimiter}At {name} ({years}) on {date} BD!",
                "404": "No birthdays found!",
                "out_of_range": "No birthday with this number was found!",
                "many_birthdays": "Too many birthdays! My database can't handle too many!",
            },
        },

        "HELP": {
            "start": "<b>/start</b> - <i>Display a welcome message.</i>",
            "help": "<b>/help</b> - <i>Display a list of commands.</i>",
            'man': '<b>/man {commands}</b> - <i>Output documentation separately for each command. Write commands without slash.</i>',
            "language": "<b>/language</b> - <i>Select communication language.</i>",
            "weather": "<b>/weather [city]</b> - <i>Display the weather forecast for today in the city city.</i>",
            "http_in_cat": "<b>/http_in_cat [*code]</b> - <i>Output a random picture with the http code or with the passed code.</i>",
            "random": "<b>/random [*end] | /random [*start] [*end]</b> - <i>Outputs a random number from 0 to 100 if no arguments are passed.\n"
                      "Outputs from 0 to end or from start to end.</i>",
            "qr_code": "<b>/qr_code [url] [*size] [*format] [*transparent]</b> - <i>Returns the QR code image on the url, size size, format (png | svg ) and transparency (true false)."
                       "Specify either 1 argument or 4 arguments.</i>",
            "birthdays": "<b>/birthdays</b> - <i>The command displays a menu with buttons for interacting with birthdays.\n</i>"
                         "<b>/birthdays list</b> - <i>Displays a list of birthdays.\n</i>" 
                         "<b>/birthdays add [name] [date] [years]</b> - <i>Add a new entry with birthday data."
                         "Name of a person (or other creature) name, date date, age years.\n</i>"
                         "<b>/birthdays change [id] [name|date|years] [arg]</b> - <i>Changes one value (name | date | years) of the id arg number record."
                         "To indicate a name consisting of more than one word, you must separate it with quotation marks \" or \'.</i>",
        },
    }
}