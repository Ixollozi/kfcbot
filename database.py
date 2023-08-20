import sqlite3
from datetime import datetime

# создаем кнопку подключения
connection = sqlite3.connect('dostavka.db')
# переводчик/исполнитель
sql = connection.cursor()

# создаем запрос на создание таблицы (пользователи,склад,корзина)

sql.execute('CREATE TABLE IF NOT EXISTS '
            'users (tg_id INTEGER,name TEXT,phone_number TEXT,address TEXT,reg_date DATETIME);')
# создаем таблицу для склада
sql.execute('CREATE TABLE IF NOT EXISTS '
            'products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT ,pr_name TEXT,pr_price REAL,'
            'pr_count INTEGER,pr_des TEXT,pr_quan INTEGER,pr_photo TEXT,date DATETIME);')
sql.execute('CREATE TABLE IF NOT EXISTS '
            'korzina (kr_id INTEGER, kr_product TEXT,'
            ' kr_quantity INTEGER, total_for_product REAL);')


# дз сделать таблицу для корзины

#### функции ####


def register_user(tg_id, name, phone_number, address):
    # создаем кнопку подключения
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    # добавляем в баззу данных пользователя

    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', (tg_id, name, phone_number, address, datetime.now()))

    # записать обновление
    connection.commit()


# проверка пользователя есть ли он в базе


def check_user(user_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    checker = sql.execute('SELECT tg_id FROM users WHERE tg_id=?;', (user_id,))
    if checker.fetchone():
        return True
    else:
        return False


def add_pr(pr_name, pr_count, pr_price, pr_des, pr_photo):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    sql.execute('INSERT INTO products (pr_name, pr_count, pr_price, pr_des, pr_photo, date) '
                'VALUES (?, ? ,? , ?, ?, ?);',
                (pr_name, pr_count, pr_price, pr_des, pr_photo, datetime.now()))
    connection.commit()


# дз удалить продуктов из склада
# удаление из склада


def delete_from_sklad():
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    sql.execute('DELETE FROM products;')
    connection.commit()


# дз удаление продукта из склада (product_id)


def delete_exact_pr_from_sklad(pr_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    sql.execute('DELETE FROM products WHERE pr_id=?;')
    connection.commit()


# получение продукта из базы данных->(name, id)


def get_pr_name_id():
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    # получаем все продукты из базы
    products = sql.execute('SELECT pr_name, pr_id, pr_count FROM products;').fetchall()
    # сортируем только те что остались
    sorted_products = [i for i in products if i[2] > 0]
    # чистый список продуктов
    return sorted_products


# получить информацию про определенный продукт (через pr_id) -> (photo,des,price)


def get_pr_id():
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    # получаем все продукты из базы
    products = sql.execute('SELECT pr_name, pr_id, pr_count FROM products;').fetchall()
    # сортируем только те что остались
    sorted_products = [i[1] for i in products if i[2] > 0]
    # чистый список продуктов
    return sorted_products


def get_exact_product(pr_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    exact_product = sql.execute('SELECT pr_photo, pr_des, pr_price FROM products WHERE pr_id=?;',
                                (pr_id,)).fetchone()
    return exact_product


# Добавление продуктов в корзину пользователя


def add_pr_to_kor(user_id, product, quantity):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    # получить цену продукта из базы
    product_price = get_exact_product(product)[2]

    sql.execute('INSERT INTO korzina (kr_id, kr_product, kr_quantity, total_for_product)'
                'VALUES (?, ?, ?, ?);', (user_id, product, quantity, quantity * product_price))
    # записать изменения
    connection.commit()

    # удаление продуктов из корзины


def delete_exact_pr_from_cart(pr_id, kr_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    sql.execute("DELETE FROM korzina WHERE kr_product=? AND kr_id=?;", (pr_id, kr_id))
    # сохранить измения
    connection.commit()


def delete_all_pr_from_cart(kr_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()
    sql.execute("DELETE FROM korzina WHERE kr_id=? ;", (kr_id, ))
    # сохранить измения
    connection.commit()

# вывод козины пользователя через (user_id) -> [(product,quantity, total_for_product)]


def get_exact_user_kor(user_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    user_kor = sql.execute("SELECT products.pr_name, "
                           " korzina.kr_quantity, "
                           "korzina.total_for_product,"
                           "korzina.kr_product FROM korzina INNER JOIN products ON "
                           "products.pr_id=korzina.kr_product"
                           " WHERE kr_id=?;", (user_id,)).fetchall()
    return user_kor
# получить номер телефона и имя юзера


def get_user_num_name(user_id):
    connection = sqlite3.connect('dostavka.db')
    # переводчик/исполнитель
    sql = connection.cursor()

    exact_user = sql.execute('SELECT name, phone_number FROM users WHERE tg_id=?;', (user_id, )).fetchone()

    return exact_user
