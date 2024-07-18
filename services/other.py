from random import choice, randint
from urllib.request import urlopen
import requests
from aiogram.types import URLInputFile

from config import config


# Прогноз погоды по API
def get_weather(city: str, lang: str = "EN"):
    # Получаем данные по openweathermap.org API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang={lang}&units=metric&appid={config.weather_api_key}"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    weather_report = None
    # Обрабатываем запрос
    if weather_response.status_code == 200:
        # Обработка полученной информации
        description = weather_data["weather"][0]["description"]
        temperature = weather_data['main']['temp']
        wind_speed = weather_data['wind']['speed']

        weather_report = (city, description, temperature, wind_speed)

    return weather_report


HTTP_CODES = [100, 101, 102, 103,
              201, 202, 203, 204, 205, 206, 207, 208, 214, 226,
              300, 301, 302, 303, 304, 305, 307, 308,
              400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 425, 426, 428, 429, 431, 444, 450, 451, 497, 498, 499,
              500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 521, 522, 523, 525, 530, 599]


# Получить случайный http код
def get_random_http() -> int:
    return choice(HTTP_CODES)


# Проверить код http на существование в HTTP_CODES
def check_http(code: int) -> int:
    return True if code in HTTP_CODES else None


# Получить изображение кота, в котором зашифрован код HTTP по API
def get_http_in_cat(code: int):
    return URLInputFile(f"https://http.cat/{code}") if check_http(code) else None


# Получить рандомное число
def get_random_number(start: int = 0, end: int = 100) -> int:
    if start > end:
        start, end = end, start
    return randint(start, end)


# Получить qr-код по API (0 - неизвестная ошибка, 1 - не открыть ресурс по url, 2 - формат файла не поддерживается)
def get_qr_code(url: str, size: int = None, file_format: str = "png", transparent: bool = False):
    """
    try:
        urlopen(url)
    except Exception:
        return 1

    file_format = file_format.lower()
    if file_format not in ("png", "svg", ".png", ".svg"):
        return 2

    transparent = "_transparent" if transparent else ""
    size = f"_{size}" if size else ""
    file_format = '.' + file_format if file_format[0] != '.' else file_format

    # print(f"https://qrtag.net/api/qr{transparent}{size}{file_format}?url={url}")
    """
    return URLInputFile(f"https://qrtag.net/api/qr{transparent}{size}{file_format}?url={url}")
