import aiosqlite as sq

from config import config


class Database:
    def __init__(self, name: str):
        self.name: str = name

    # Создаём таблицы, если они ещё не созданы
    async def create_tables(self):
        async with sq.connect(self.name) as connection:
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY
                );
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT
                );
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS birthdays (
                birthday_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                date DATE,
                years INTEGER
                );
            """)

            await connection.commit()

    async def add_user(self, user_id: int):
        async with sq.connect(self.name) as connection:
            await connection.execute("INSERT INTO users VALUES(?, ?);", (user_id, config.default_language))
            await connection.commit()

    async def delete_user(self, user_id: int):
        async with sq.connect(self.name) as connection:
            await connection.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            await connection.commit()

    async def get_user(self, user_id: int) -> tuple:
        async with sq.connect(self.name) as connection:
            async with connection.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,)) as cursor:
                return await cursor.fetchone()

    async def set_language(self, user_id: int, language: str):
        async with sq.connect(self.name) as connection:
            await connection.execute(f"UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
            await connection.commit()

    async def get_language(self, user_id: int) -> str:
        async with sq.connect(self.name) as connection:
            async with connection.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)) as cursor:
                language: tuple = await cursor.fetchone()
                if not language:
                    return ""
                return language[0]


db: Database = Database("db.sql")


'''
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
'''