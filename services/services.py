"""

import random

from lexicon.lexicon_ru import LEXICON_RU


# Функция, возвращающая случайный выбор бота в игре
def get_bot_choice() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


# Функция, возвращающая ключ из словаря, по которому
# хранится значение, передаваемое как аргумент - выбор пользователя
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


# Функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules = {'rock': 'scissors',
             'scissors': 'paper',
             'paper': 'rock'}
    if user_choice == bot_choice:
        return 'nobody_won'
    elif rules[user_choice] == bot_choice:
        return 'user_won'
    return 'bot_won'

# Прогноз погоды по API
def get_weather(city: str) -> str:
    # Координаты города: Saint Petersburg, Russia
    lat = 59.9375
    long = 30.3086

    # Получаем данные по Open-Meteo API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if weather_response.status_code == 200 and "current_weather" in weather_data:
        # Обработка полученной информации
        temperature = weather_data['current_weather']['temperature']
        wind_speed = weather_data['current_weather']['windspeed']
        weather_code = weather_data['current_weather']['weathercode']

        # Добавление описания
        weather_descriptions = {
            0: "Ясно. Понятно?",
            1: "Преимущественно ясно, но не очень",
            2: "Переменная облачность. Тучи. Но немного",
            3: "Пасмурно. Тучи, много туч",
            45: "Туман. Как обычно в Петербурге и в Лондоне",
            48: "Гололедный туман. Мало того, что туман, так и гололед",
            51: "Легкая морось. Капает, но мало",
            53: "Умеренная морось. Капает. Уже не мало",
            55: "Сильная морось. Сильно капает",
            56: "Легкая ледяная морось. Замерзло и капает",
            57: "Сильная ледяная морось. Замерзло и сильно капает",
            61: "Небольшой дождь. Норм, без зонта",
            63: "Умеренный дождь. Нужен зонт",
            65: "Сильный дождь. Сиди дома",
            66: "Легкий ледяной дождь",
            67: "Сильный ледяной дождь. Не просто дождь, а ледяной!",
            71: "Небольшой снегопад. Чуть-чуть",
            73: "Умеренный снегопад. Снег, но не прямо много",
            75: "Сильный снегопад. Очень много снега",
            77: "Снежные зерна",
            80: "Небольшие ливни. Когда льёт как из ведра, но маленького",
            81: "Умеренные ливни. Когда льёт как из ведра, среднего",
            82: "Сильные ливни. Когда льёт как из ведра, большого",
            85: "Небольшие снеговые ливни",
            86: "Сильные снеговые ливни. Ужас какой-то",
            95: "Гроза. Очень шумно",
            96: "Гроза с легким градом. Как будто одной грозы мало",
            99: "Гроза с сильным градом. Шумно и больно",
        }
        weather_description = weather_descriptions.get(weather_code, "Непонятная погода")

        weather_report = (
            f"Погода в нашем городе сейчас такая:\n"
            f"Чего ждать: {weather_description}\n"
            f"Температура по цельсию: {temperature:.1f}°C\n"
            f"Скорость ветра: {wind_speed:.1f} м/с, так что не улетишь"
        )
    else:
        weather_report = "Не могу понять, что за погода"

    return weather_report

"""