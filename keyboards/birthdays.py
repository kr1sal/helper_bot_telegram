from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import LEXICON

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