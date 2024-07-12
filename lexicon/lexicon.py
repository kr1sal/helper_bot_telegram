LEXICON: dict = {
    # Русский
    "RU": {
        "BASE": {
            'other_answer': 'Извини, увы, это сообщение мне непонятно...',
            "not_found": "Команда не найдена!",
            "invalid": "Неправильный синтаксис команды!",
            "wrong_args": "Неверное количество переданных аргументов!",
            "tech_work": "Технические шоколадки!",
        },
        "COMMANDS": {
            'start': '<b>Привет!\nЯ виртуальный помощник</b>\n\nЧтобы получить список комманд введите /help\n\nДля смены языка введите /language',
            'man': 'Справка: [аргумент] {множество аргументов} [*аргумент], где *необязательный',
            'language': "Выберите язык!",
        },
        "HELP": {
            "start": "/start - Вывести приветственное сообщение",
            "help": "/help - Вывести список команд",
            'man': '/man {commands} - Вывести документацию отдельно для каждой команды. Пишите команды без слеша',
            "language": "/language - Выбрать язык коммуникации",
            "weather": "/weather [city] - Вывести прогноз погоды на сегодня в городе city",
            "http_in_cat": "/http_in_cat [*code] - Вывести случайную картинку с кодом http или с переданным code",
            "random": "/random [*end] | /random [*start] [*end] - Выводит рандомное число от 0 до 100, если не переданы аргументы. Выводит от 0 до end или от start до end",
            "qr_code": "/qr_code [url] [*size] [*format] [*transparent] - Возвращает изображение QR-кода на url, размером size, форматом format (png | svg) и прозрачностью (true false). Указывайте либо 1 аргумент, либо 4 аргумента"
        },
        "SERVICES": {
            "change_language": "Вы сменили язык: {language_old} ==> {language}",
            "404": "Ошибка 404! Код HTTP не найден!",
            "wrong_url": "Указан неверный url. Перепроверьте ссылку!",
            "wrong_file_format": "Неверный формат файла {format_file}!",
            "weather": {
                "main": "Погода в <b>{city}</b> сейчас такая:",
                "description": "За окном: <b>{description}</b>",
                "temperature": "Температура: <b>{temperature}°C</b>",
                "wind_speed": "Скорость ветра: <b>{wind_speed}</b> м/с"
            },
            "city_not_found": "Невозможно определить погоду для <b>{city}</b>"
        }
    },

    # English, just English
    "EN": {
        "BASE": {
            'other_answer': "Sorry, i don't understand!",
            "not_found": "Command not found!",
            "invalid": "Invalid syntax!",
            "wrong_args": "Invalid number of arguments passed!",
            "tech_work": "Technical chocolates!",
        },
        "COMMANDS": {
            'start': "<b>Hi!\nI'm a virtual assistant</b>\n\nTo get a list of commands, enter /help\n\nTo change the language, enter /language",
            'man': 'Manual: [argument] {many arguments} [*argument], where *optional',
            'language': "Choose language!",
        },
        "HELP": {
            "start": "/start - Display a welcome message",
            "help": "/help - Display a list of command",
            'man': '/man {commands} - Output documentation separately for each command. Write commands without slashes',
            "language": "/language - Select communication language",
            "weather": "/weather [city] - Display the weather forecast for today in the city",
            "http_in_cat": "/http_in_cat [*code] - Display a random picture with the http code or the transmitted code",
            "random": "/random [*end] | /random [*start] [*end] - Prints a random number from 0 to 100 if no arguments are passed. Prints from 0 to end or from start to end",
            "qr_code": "/qr_code [url] [*size] [*format] [*transparent] - Returns a QR code image at url, size size, format (png | svg) and transparency (true false). Specify either 1 argument or 4 arguments"
        },
        "SERVICES": {
            "change_language": "You changed your language: {language_old} ==> {language}",
            "404": "Error 404! HTTP code not found!",
            "wrong_url": "Invalid url specified. Double check the link!",
            "wrong_file_format": "Wrong file format!",
            "weather": {
                "main": "Whether in <b>{city}</b> now:",
                "description": "Outside: <b>{description}</b>",
                "temperature": "Temperature: <b>{temperature}°C</b>",
                "wind_speed": "Wind speed: <b>{wind_speed}</b> м/с"
            },
            "city_not_found": "It is impossible to determine the weather for <b>{city}</b>"
        }
    }
}