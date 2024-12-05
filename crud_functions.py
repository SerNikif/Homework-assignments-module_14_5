import sqlite3

connection = sqlite3.connect('Products.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )''')
    connection.commit()


initiate_db()


def get_all_products():
    cursor.execute("SELECT * FROM Products WHERE id = ?", (id,))
    connection.commit()
    prod = cursor.fetchall()
    title, description, price = prod[0]
    return f"Название: {title} | Описание: {description} | Цена: {price}"


connection.commit()
connection.close()


connection = sqlite3.connect('users.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
);
''')


def add_user(username, email, age):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'{username}', f'{email}', f'{age}', f'{1000}'))
    connection.commit()


def is_included(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    check_users = cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    if check_users.fetchone() is None:
        return False
    else:
        return True


connection.commit()
connection.close()