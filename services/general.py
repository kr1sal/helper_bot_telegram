from re import split
from aiogram import Bot


# Преобразовать строку с командой в аргументы
def get_args(string: str) -> list[str]:
    args: list[str] = []

    word = ""
    merge = False
    for c in string:
        if c != "\'" and c != "\"":
            if c != " " or merge:
                word += c
            elif word and not merge:
                args.append(word)
                word = ""
        else:
            merge = not merge

    if word:
        args.append(word)

    return args


# Выводит список из разделённых строк с помощью множества разделителей
def multi_split(separators: list[str], string: str) -> list[str]:
    return split(f"[{''.join(separators)}]", string.strip())


# Отправить сообщение пользователю
async def send_message(bot: Bot, chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)
