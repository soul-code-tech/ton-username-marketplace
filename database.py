import sqlite3
import os

DB_PATH = "usernames.db"

def init_db():
    """Создаёт таблицу, если её нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            seller_id INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT DEFAULT 'active'
        )
    ''')
    conn.commit()
    conn.close()

def add_listing(username, seller_id, price):
    """Добавляет лот в базу"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO listings (username, seller_id, price) VALUES (?, ?, ?)',
            (username, seller_id, price)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_listings():
    """Возвращает все активные лоты"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT username, price, seller_id FROM listings WHERE status = "active"')
    listings = cursor.fetchall()
    conn.close()
    return listings

def get_listing_by_username(username):
    """Возвращает лот по username"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT price, seller_id FROM listings WHERE username = ? AND status = "active"', (username,))
    result = cursor.fetchone()
    conn.close()
    return result

def deactivate_listing(username):
    """Деактивирует лот (после продажи)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE listings SET status = "sold" WHERE username = ?', (username,))
    conn.commit()
    conn.close()
