import sqlite3 as sq


class Database:
    # Соединяемся с базой данных
    def __init__(self):
        self.connection = sq.connect("db.sql")
        self.cursor = self.connection.cursor()
        # Описываем базу данных
        # Never do this -- insecure!
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            language TEXT,
            birthdays TEXT
            )
        """)
        self.connection.commit()

    # Завершаем работу с базой данных
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # Добавляем нового пользователя в дб
    def add_user(self, user_id) -> bool:
        # Извлекаем данные пользователя
        user = self.cursor.execute(f"SELECT 1 FROM users WHERE user_id == {user_id};").fetchone()
        # если пользователь не существует, то добавить в дб
        if not user:
            self.cursor.execute("INSERT INTO users VALUES(?, ?, ?);", (user_id, "EN", ""))
            self.connection.commit()
            return False

        return True

    # Меняет язык общения и возвращает старый
    def change_language(self, user_id, language) -> str:
        # Получаем старый язык пользователя
        language_old = self.cursor.execute(f"SELECT language FROM users WHERE user_id == {user_id}").fetchone()[0]
        # Меняем язык
        self.cursor.execute(f"UPDATE users SET language='{language}' WHERE user_id == {user_id}")
        self.connection.commit()

        return language_old

    # Получить язык пользователя
    def get_language(self, user_id) -> str:
        # Получаем язык пользователя
        language = self.cursor.execute(f"SELECT language FROM users WHERE user_id == {user_id}").fetchone()[0]

        return language
