from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON

""" LANGUAGES """

# Получаем все языки из lexicon.py и создаём кнопки с ними
language_buttons = []
for lang in LEXICON.keys():
    language_buttons.append(InlineKeyboardButton(
        text=LEXICON[lang]["name"],
        callback_data=f"{lang}_button_pressed"
    ))

# Создаём клавиатуру с выбором языка
language_kb = InlineKeyboardMarkup(
    inline_keyboard=[language_buttons]
)

""" BIRTHDAYS"""

# Основное меню birthdays
# Кнопка добавления нового дня рождения
add_birthday_button = InlineKeyboardButton(
    text='Add birthday',
    callback_data='add_birthday_button_pressed'
)

# Кнопка добавления нового дня рождения
edit_birthday_button = InlineKeyboardButton(
    text='Edit birthday',
    callback_data='edit_birthday_button_pressed'
)

# Кнопка появления календаря
birthdays_calendar_button = InlineKeyboardButton(
    text='Birthdays Calendar',
    callback_data='birthdays_calendar_button_pressed'
)

# Клавиатура основного меню birthdays
birthdays_kb = InlineKeyboardMarkup(
    inline_keyboard=[[add_birthday_button, edit_birthday_button],
                     [birthdays_calendar_button]]
)

# Редактор дня рождения
# Кнопка смены имени дня рождении
change_name_button = InlineKeyboardButton(
    text='name',
    callback_data='change_name_button_pressed'
)

# Кнопка смены даты
change_date_button = InlineKeyboardButton(
    text='date',
    callback_data='change_date_button_pressed'
)

# Кнопка смены времени
change_time_button = InlineKeyboardButton(
    text='time',
    callback_data='change_time_button_pressed'
)

# Кнопка смены возраста
change_years_button = InlineKeyboardButton(
    text='years',
    callback_data='change_years_button_pressed'
)

# Кнопка смены возраста
delete_birthday_button = InlineKeyboardButton(
    text='delete_birthday',
    callback_data='delete_birthday_button_pressed'
)

# Клавиатура изменения дня рождения
edit_birthday_kb = InlineKeyboardMarkup(
    inline_keyboard=[[change_name_button, change_date_button],
                     [change_time_button, change_years_button],
                     [delete_birthday_button]]
)

# Календарь birthdays
# pass

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
