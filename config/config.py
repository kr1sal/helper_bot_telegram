import logging

from dataclasses import dataclass
from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class Config:
    default_language: str
    bot_token: str
    weather_api_key: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(default_language="en",
                  bot_token=env("BOT_TOKEN"),
                  weather_api_key=env("WEATHER_API_KEY"))


config: Config = load_config()
