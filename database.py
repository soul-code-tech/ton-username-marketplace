import sqlite3

def init_db():
    conn = sqlite3.connect('usernames.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            seller_id INTEGER,
            price REAL,
            status TEXT DEFAULT 'active'
        )
    ''')
    conn.commit()
    conn.close()

def add_listing(username, seller_id, price):
    conn = sqlite3.connect('usernames.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO listings (username, seller_id, price) VALUES (?, ?, ?)', (username, seller_id, price))
    conn.commit()
    conn.close()

def get_listings():
    conn = sqlite3.connect('usernames.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, price, seller_id FROM listings WHERE status = "active"')
    return cursor.fetchall()
