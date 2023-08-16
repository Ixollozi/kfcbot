
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# кнопки со всеми продуктами(основное меню)


def main_menu_kb(products_from_db):
    kb = InlineKeyboardMarkup(row_width=2)
    # незгораемые кнопки
    order = InlineKeyboardButton(text='офромить заказ', callback_data="order")
    cart = InlineKeyboardButton(text="корзина", callback_data='cart',)
    next_pag = InlineKeyboardButton(text='следующая страница', callback_data='next')
    # промежуточные кнопки(кнопки с товаром(берем из базы))
    # создаем кнопки с продуктами
    all_pr = [InlineKeyboardButton(text=i[0], callback_data=i[1]) for i in products_from_db if i[1] <= 10]

    # добавить в пространство
    kb.row(order)
    kb.add(*all_pr)
    kb.row(next_pag)
    kb.row(cart)
    return kb


# кнопки для выбора количества
def choose_product_count(plus_or_minus='', current_amount=1):
    kb = InlineKeyboardMarkup(row_width=3)
    # незгораемая кнопка
    back = InlineKeyboardButton(text="назад", callback_data="back")
    plus = InlineKeyboardButton(text="+", callback_data="increment")
    minus = InlineKeyboardButton(text="-", callback_data="decrement")
    count = InlineKeyboardButton(text=str(current_amount), callback_data='asd')
    add_to_cart = InlineKeyboardButton(text="добавить в корзину", callback_data="add_to_cart")
    # создаем сами кнопки -/+
    # отслеживаем плюс или минус
    if plus_or_minus == "increment":
        new_amount = int(current_amount)+1
        count = InlineKeyboardButton(text=str(new_amount), callback_data='asd')
    elif plus_or_minus == 'descrement':
        if int(current_amount) != 1:
            new_amount = int(current_amount) - 1
            count = InlineKeyboardButton(text=str(new_amount), callback_data='asd')
    # обьеденияем простраства
    kb.add(minus, count, plus)
    kb.row(add_to_cart)
    kb.row(back)
    # возращаем кнопки
    return kb

# кнопка для регистрации то есть отправка номера


def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    number = KeyboardButton("поделиться контактом", request_contact=True)
    kb.add(number)
    return kb


def loc_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    loc = KeyboardButton("поделиться локацией", request_location=True)
    kb.add(loc)

    return kb

# кнопки для потверждения для заказа


def get_accept_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    yes = KeyboardButton("потвердить")
    no = KeyboardButton("отменить")
    kb.add(yes, no)

    return kb


def delete_from_cart():
    kb = InlineKeyboardMarkup(row_width=1)
    delete = InlineKeyboardButton(text="удалить продукт", callback_data="delete")
    back = InlineKeyboardButton(text='назад', callback_data='back')
    al = InlineKeyboardButton(text="удалить все продукты из корзины", callback_data="al")
    kb.row(delete)
    kb.row(al)
    kb.row(back)

    return kb


def delete_menu_kb(korzina_from_db):
    kb = InlineKeyboardMarkup(row_width=True)
    # создаем кнопки с продуктами
    all_pr = [InlineKeyboardButton(text=f'❌ {i[0]}', callback_data=f'❌{i[3]}') for i in korzina_from_db]
    back = InlineKeyboardButton(text='назад', callback_data='back')
    # добавить в пространство
    kb.add(*all_pr)
    kb.row(back)
    return kb


def next_page(products_from_db):

    kb = InlineKeyboardMarkup(row_width=2)
    order = InlineKeyboardButton(text='офромить заказ', callback_data="order")
    cart = InlineKeyboardButton(text="корзина", callback_data='cart', )
    all_pr = [InlineKeyboardButton(text=i[0], callback_data=i[1]) for i in products_from_db if
              i[1] > 10 or i[1] > 20]
    page_bef = InlineKeyboardButton(text='предыдущая страница', callback_data='page_bef')

    next_pag = InlineKeyboardButton(text='следующая страница', callback_data='next')
    kb.row(order)
    kb.add(*all_pr)
    kb.row(page_bef, next_pag)
    kb.row(cart)
    return kb
