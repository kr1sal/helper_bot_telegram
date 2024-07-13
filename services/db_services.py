import sqlite3 as sq
import datetime as dt


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
            birthday_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            date DATE,
            time TIME,
            years INTEGER
            );
        """)
        self.connection.commit()

    # Завершаем работу с базой данных
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # Добавляем нового пользователя в дб
    def add_user(self, user_id) -> bool:
        # Извлекаем данные пользователя
        user = self.cursor.execute(f"SELECT 1 FROM users WHERE user_id = ?;", (user_id,)).fetchone()
        # если пользователь не существует, то добавить в дб
        if not user:
            self.cursor.execute("INSERT INTO users VALUES(?, ?);", (user_id, "EN"))
            self.connection.commit()
            return False

        return True

    """ LANGUAGES """

    # Меняет язык общения и возвращает старый
    def change_language(self, user_id, language) -> str:
        # Получаем старый язык пользователя
        language_old = self.cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        # Меняем язык
        self.cursor.execute(f"UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
        self.connection.commit()

        return language_old

    # Получить язык пользователя
    def get_language(self, user_id) -> str:
        # Получаем язык пользователя
        language = self.cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]

        return language

    """ BIRTHDAYS """

    # Добавить день рождение в базу (уникальный name)
    def add_birthday(self, user_id, name, date, time, years):
        self.cursor.execute("INSERT INTO birthdays(user_id, name, date, time, years) VALUES(?, ?, ?, ?, ?);", (user_id, name, date, time, years))
        self.connection.commit()

    # Получить день рождение по имени кортежем
    def get_birthday(self, birthday_id, name):
        # Извлекаем данные о дне рождении
        birthday = self.cursor.execute("SELECT * FROM birthdays WHERE birthday_id = ?;", (birthday_id,)).fetchall()

        return birthday

    # Получить все дни рождения пользователя списком
    def get_user_birthdays(self, user_id):
        birthdays = self.cursor.execute("SELECT * FROM birthdays WHERE user_id = ?;", (user_id,)).fetchall()

        return birthdays
