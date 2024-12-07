import sqlite3
import requests
from io import BytesIO
from PIL import Image


def init_db():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER UNIQUE,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    photo BLOB, 
                    search INTEGER DEFAULT 1
                )''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()


def check_user_exists(telegram_id):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM users WHERE telegram_id = ?', (telegram_id,))
            return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False


def add_user(telegram_id, username, first_name, last_name, photo):
    if check_user_exists(telegram_id):
        return
    
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO users (telegram_id, username, first_name, last_name, photo)
            VALUES (?, ?, ?, ?, ?)
            ''', (telegram_id, username, first_name, last_name, photo))
            conn.commit()
            print("Пользователь добавлен успешно!")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")


def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if user:
        username = user[2]  
        full_name = f"{user[3]} {user[4]}"  
        photo_url = user[5]  

        response = requests.get(photo_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return full_name, image, username
        else:
            return full_name, None
    else:
        return None, None
    


def get_random_user(exclude_user_id=None):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        query = 'SELECT * FROM users'
        if exclude_user_id:
            query += ' WHERE telegram_id != ?'

        c.execute(query, (exclude_user_id,)) if exclude_user_id else c.execute(query)

        user = c.fetchone()  

        if user:
            telegram_id = user[1] 
            return telegram_id

        else:
            print("Нет пользователей в базе данных.")
            
    except sqlite3.Error as e:
        print(f"Ошибка при получении случайного пользователя: {e}")
    finally:
        if conn:
            conn.close()

        



