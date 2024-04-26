import sqlite3
import os

# -------------------
# создаем базы данных
# -------------------


# все файлы БД

# папка
databases_dir = os.path.dirname(__file__)

# файлы БД
stats_db = os.path.join(databases_dir, 'gamblers.db')


# все пользователи и их настройки
def users_table_creation():
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                       user_id INT,
                       money INT,
                       tries INT,
                       was_lucky INT, 
                       last_time_of_usage STRING
                       )""")
        db.commit()


# --------------------------------------
# дописываем и/или обновляем данные в БД
# --------------------------------------


# новый пользователь, добавляем его в общую базу
def new_user(user_id, time):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT user_id 
                       FROM users 
                       WHERE user_id = ?""",
                       [user_id])
        already_exists = cursor.fetchone()
        if already_exists is None:
            cursor.execute("""INSERT INTO users
                           (user_id, money, tries, was_lucky, last_time_of_usage) 
                           VALUES(?, ?, ?, ?, ?)""",
                           [user_id, 0, 0, 0, time])
        db.commit()


# переписываю --историю-- стату
def new_krutochka(user_id, won, time):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT tries, was_lucky
                               FROM users
                               WHERE user_id = ?""",
                       [user_id])
        tries, was_lucky = cursor.fetchall()[0]
        cursor.execute("""UPDATE users
                       SET (tries, was_lucky, last_time_of_usage) = (?, ?, ?)
                       WHERE user_id = ?""",
                       [tries + 1, was_lucky + 1 if won else was_lucky, time, user_id])
        db.commit()


# ----------------------------
# достаем из баз нужные данные
# ----------------------------


# данные пользователя
def data(user_id):
    with sqlite3.connect(stats_db) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT money, tries, was_lucky, last_time_of_usage
                       FROM users
                       WHERE user_id = ?""",
                       [user_id])
        stats = cursor.fetchall()
    return stats[0]


if __name__ == '__main__':
    users_table_creation()
