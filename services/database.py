import sqlite3 as sq
import datetime as dt

from config import config

sq.register_adapter(bool, int)


class Database:
    # Соединяемся с базой данных
    def __init__(self):
        self.connection = sq.connect("db.sql")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT
            );
        """)

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
    async def add_user(self, user_id: int) -> bool:
        user = self.cursor.execute("SELECT 1 FROM users WHERE user_id = ?;",
                                   (user_id,)).fetchone()
        # если пользователь не существует, то добавить в дб и вернуть True, иначе False
        if not user:
            self.cursor.execute("INSERT INTO users VALUES(?, ?);",
                                (user_id, config.default_language))
            self.connection.commit()
            return True

        return False

    # Проверяет, существует ли пользователь
    async def get_user(self, user_id: int) -> list | None:
        user = self.cursor.execute("SELECT * FROM users WHERE user_id = ?;",
                                   (user_id,)).fetchone()
        return user

    # Удаляет пользователя из базы данных
    async def delete_user(self, user_id: int):
        self.cursor.execute("DELETE FROM users WHERE user_id = ?",
                            (user_id,))

    """ LANGUAGES """
    # Устанавливает язык общения
    async def set_language(self, user_id: int, language: str):
        self.cursor.execute(f"UPDATE users SET language = ? WHERE user_id = ?",
                            (language, user_id))
        self.connection.commit()

    # Меняет язык общения и возвращает старый
    async def change_language(self, user_id: int, language: str) -> str | None:
        # Получаем старый язык пользователя
        language_old = self.cursor.execute("SELECT language FROM users WHERE user_id = ?",
                                           (user_id,)).fetchone()
        # Меняем язык
        self.cursor.execute(f"UPDATE users SET language = ? WHERE user_id = ?",
                            (language, user_id))
        self.connection.commit()

        if not language_old:
            return

        return language_old[0]

    # Получить язык пользователя
    async def get_language(self, user_id: int) -> str | None:
        language = self.cursor.execute("SELECT language FROM users WHERE user_id = ?",
                                       (user_id,)).fetchone()
        if not language:
            return

        return language[0]

    """ BIRTHDAYS """

    # Добавить день рождение в базу (уникальный name)
    async def add_birthday(self, user_id: int, name: str, date: dt.date, years: int, remind: bool = True) -> int:
        birthday_id = self.cursor.execute("INSERT INTO birthdays(user_id, name, date, years) VALUES(?, ?, ?, ?, ?)"
                                          "RETURNING birthday_id;",
                                          (user_id, name, date, years, remind)).fetchone()[0]
        self.connection.commit()
        return birthday_id

    # Изменить имя дня рождения
    async def set_name_birthday(self, birthday_id: int, name: str):
        self.cursor.execute("UPDATE birthdays SET name = ? WHERE birthday_id = ?;",
                            (name, birthday_id))
        self.connection.commit()

    # Изменить дату дня рождения
    async def set_date_birthday(self, birthday_id: int, date: dt.date):
        self.cursor.execute("UPDATE birthdays SET date = ? WHERE birthday_id = ?;",
                            (date, birthday_id))
        self.connection.commit()

    # Изменить возраст дня рождения
    async def set_years_birthday(self, birthday_id: int, years: int):
        self.cursor.execute("UPDATE birthdays SET years = ? WHERE birthday_id = ?;",
                            (years, birthday_id))
        self.connection.commit()

    # Получить день рождение по имени кортежем
    async def get_birthday(self, birthday_id: int) -> list | None:
        # Извлекаем данные о дне рождении
        birthday: list = self.cursor.execute("SELECT * FROM birthdays WHERE birthday_id = ?;",
                                             (birthday_id,)).fetchall()
        return birthday

    # Получить все дни рождения пользователя списком кортежей
    async def get_user_birthdays(self, user_id: int) -> list | None:
        birthdays: list = self.cursor.execute("SELECT * FROM birthdays WHERE user_id = ?;",
                                              (user_id,)).fetchall()
        return birthdays

    # Удалить день рождение из базы данных
    async def delete_birthday(self, birthday_id: int):
        self.cursor.execute("DELETE FROM birthdays WHERE birthday_id = ?;",
                            (birthday_id,))


db = Database()
