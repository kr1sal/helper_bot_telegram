import sqlite3 as sq
import datetime as dt
from typing import List, Any


class Database:
    # Соединяемся с базой данных
    def __init__(self):
        self.connection = sq.connect("db.sql")
        self.cursor = self.connection.cursor()

        # Описываем базу данных users
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT
            );
        """)
        # Описываем базу данных birthdays
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS birthdays (
            birthday_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            date DATE,
            years INTEGER
            );
        """)
        self.connection.commit()

    # Завершаем работу с базой данных
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # Добавляем нового пользователя в дб
    async def add_user(self, user_id: int) -> None:
        # Извлекаем данные пользователя
        user = self.cursor.execute(f"SELECT 1 FROM users WHERE user_id = ?;",
                                   (user_id,)).fetchone()
        # если пользователь не существует, то добавить в дб
        if not user:
            self.cursor.execute("INSERT INTO users VALUES(?, ?);",
                                (user_id, "EN"))
            self.connection.commit()

    """ LANGUAGES """

    # Меняет язык общения и возвращает старый
    async def change_language(self, user_id: int, language: str) -> str:
        # Получаем старый язык пользователя
        language_old = self.cursor.execute("SELECT language FROM users WHERE user_id = ?",
                                           (user_id,)).fetchone()[0]
        # Меняем язык
        self.cursor.execute(f"UPDATE users SET language = ? WHERE user_id = ?",
                            (language, user_id))
        self.connection.commit()

        return language_old

    # Получить язык пользователя
    async def get_language(self, user_id: int) -> str:
        # Получаем язык пользователя
        language = self.cursor.execute("SELECT language FROM users WHERE user_id = ?",
                                       (user_id,)).fetchone()[0]

        return language

    """ BIRTHDAYS """

    # Добавить день рождение в базу (уникальный name)
    async def add_birthday(self, user_id: int, name: str, date: dt.date, years: int) -> None:
        self.cursor.execute("INSERT INTO birthdays(user_id, name, date, years) VALUES(?, ?, ?, ?);",
                            (user_id, name, date, years))
        self.connection.commit()

    # Изменить имя дня рождения
    async def change_name_birthday(self, birthday_id: int, name: str) -> None:
        self.cursor.execute("UPDATE birthdays SET name = ? WHERE birthday_id = ?;",
                            (name, birthday_id))
        self.connection.commit()

    # Изменить дату дня рождения
    async def change_date_birthday(self, birthday_id: int, date: dt.date) -> None:
        self.cursor.execute("UPDATE birthdays SET date = ? WHERE birthday_id = ?;",
                            (date, birthday_id))
        self.connection.commit()

    # Изменить возраст дня рождения
    async def change_years_birthday(self, birthday_id: int, years: int) -> None:
        self.cursor.execute("UPDATE birthdays SET years = ? WHERE birthday_id = ?;",
                            (years, birthday_id))
        self.connection.commit()

    # Получить день рождение по имени кортежем
    async def get_birthday(self, birthday_id: int) -> List[Any]:
        # Извлекаем данные о дне рождении
        birthday: list[Any] = self.cursor.execute("SELECT * FROM birthdays WHERE birthday_id = ?;",
                                                  (birthday_id,)).fetchall()
        return birthday

    # Получить все дни рождения пользователя списком кортежей
    async def get_user_birthdays(self, user_id: int) -> List[Any]:
        birthdays: list[Any] = self.cursor.execute("SELECT * FROM birthdays WHERE user_id = ?;",
                                                   (user_id,)).fetchall()
        return birthdays

    # Удалить день рождение из базы данных
    async def delete_birthday(self, birthday_id: int) -> None:
        self.cursor.execute("DELETE FROM birthdays WHERE birthday_id = ?;",
                            (birthday_id,))
