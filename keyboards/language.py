from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import LEXICON

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