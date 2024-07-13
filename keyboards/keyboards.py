from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# from lexicon.lexicon_ru import KEYBOARDS

""" LANGUAGES """

# Кнопки выбора языка
# Russian
ru_button = InlineKeyboardButton(
    text='Русский',
    callback_data='ru_button_pressed'
)
# English
en_button = InlineKeyboardButton(
    text='English',
    callback_data='en_button_pressed'
)

# Создаём клавиатуру с выбором языка
language_kb = InlineKeyboardMarkup(
    inline_keyboard=[[ru_button],
                     [en_button]]
)

""" BIRTHDAYS"""


"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon_ru import KEYBOARDS


# Создаем кнопки клавиатуры
kb_button_1 = KeyboardButton(text=KEYBOARDS['weather'])
kb_button_2 = KeyboardButton(text=KEYBOARDS['tasks'])
kb_button_3 = KeyboardButton(text=KEYBOARDS['happy'])

# Создаем клавиатуру функций
helper_kb = ReplyKeyboardMarkup(
    keyboard=[[kb_button_1],
              [kb_button_2],
              [kb_button_3]],
    resize_keyboard=True
)

task_button_1 = KeyboardButton(text=KEYBOARDS['add_task'])
task_button_2 = KeyboardButton(text=KEYBOARDS['show_task'])
task_button_3 = KeyboardButton(text=KEYBOARDS['back'])

# Создаем объект клавиатуры для задач
tasks_kb = ReplyKeyboardMarkup(
    keyboard=[[task_button_1],
              [task_button_2],
              [task_button_3]],
    resize_keyboard=True,
    input_field_placeholder='Используйте /add_task для добавления задачи, /list для просмотра задач и /clear для удаления всех задач.'
)

weather_button_1 = KeyboardButton(text=KEYBOARDS['ask_weather'])
weather_button_2 = KeyboardButton(text=KEYBOARDS['back'])

weather_kb = ReplyKeyboardMarkup(
    keyboard=[[weather_button_1],
              [weather_button_2]],
    resize_keyboard=True,
    input_field_placeholder='Нажмите узнать погоду'
)

happy_button_1 = KeyboardButton(text=KEYBOARDS['gen_joke'])
happy_button_2 = KeyboardButton(text=KEYBOARDS['back'])


happy_kb = ReplyKeyboardMarkup(
    keyboard=[[happy_button_1],
              [happy_button_2]],
    resize_keyboard=True,
    input_field_placeholder='Нажмите кнопку, чтобы сгенерировать шутку'
)


"""