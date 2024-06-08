BASE: dict[str, str] = {
    'other_answer': 'Извини, увы, это сообщение мне непонятно...',
    "not_found": "Команда не найдена!",
    "invalid": "Неправильный синтаксис команды!",
    "wrong_args": "Неверное количество переданных аргументов!",
    "tech_work": "Технические шоколадки!",
}

COMMANDS: dict[str, str] = {
    'start': '<b>Привет!\nЯ виртуальный помощник</b>\n\nЧтобы получить список комманд введите /help\n\nДля смены языка введите /language',
    'man': 'Справка: [аргумент] {множество аргументов} [*аргумент], где *необязательный',
    'language': "Выберите язык!",
}

HELP: dict[str, str] = {
    "start": "/start - Вывести приветственное сообщение",
    "help": "/help - Вывести список команд",
    'man': '/man {commands} - Вывести документацию отдельно для каждой команды. Пишите команды без слеша',
    "language": "/language - Выбрать язык коммуникации",
    "weather": "/weather [*city] - Вывести прогноз погоды на сегодня в городе city",
    "http_in_cat": "/http_in_cat [*code] - Вывести случайную картинку с кодом http или с переданным code",
    "random": "/random [*end] | /random [*start] [*end] - Выводит рандомное число от 0 до 100, если не переданы аргументы. Выводит от 0 до end или от start до end",
    "qr_code": "/qr_code [url] [*size] [*format] [*transparent] - Возвращает изображение QR-кода на url, размером size, форматом format (png | svg) и прозрачностью (true false). Указывайте либо 1 аргумент, либо 4 аргумента"
}

SERVICES: dict[str, str] = {
    "404": "Ошибка 404! Код HTTP не найден!",
    "wrong_url": "Указан неверный url. Перепроверьте ссылку!"
}
