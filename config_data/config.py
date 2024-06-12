from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    bot_token: str
    weather_api_key: str


# Инициализируем среду переменных и загружаем конфиг в переменную config
env = Env()
env.read_env()
config: Config = Config(bot_token=env("BOT_TOKEN"),
                        weather_api_key=env("WEATHER_API_KEY"))
