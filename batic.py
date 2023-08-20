import database
import butt
import telebot
import config
from telebot.types import ReplyKeyboardRemove
from geopy.geocoders import Nominatim
from telebot import types
# словарь для временных данных
users = {}
#
# database.add_pr('лонгер', 10, 25000, 'мощни сочни восточни',
#                 'https://kfs-menu.ru/images/menu/longer.jpg')
# database.add_pr('куриные крылышки', 15, 35000, 'острые',
#                 'https://mcdonaldsmenu.ru/image/cache/catalog/photo/121248146-kurinye-krylyshki-600x600.png')
# database.add_pr('соус терияки', 1, 50000, 'легенда',
#                 'https://makkam.ru/d/sous_teriyaki-01.png')
# database.add_pr('чизбургер', 2, 25000, 'мощни сочни восточни',
#                 'https://s82079.cdn.ngenix.net/295x0/vghkltjf1l05c2zlvxpx3hw8xg7v')
# database.add_pr('малиновые пирожки', 13, 25000, 'мощни сочни восточни',
#                 'https://s82079.cdn.ngenix.net/295x0/sktp4fzwf87bynddn9k3k92jt5bc')
# database.add_pr('клубничные пирожки', 14, 12000, 'мощни сочни восточни',
#                 'https://kfs-menu.ru/images/menu/pirozhok-klubnika-slivochnyy-syr.zrzg1wqetpw4ups3p9x6p6d0owie')
# database.add_pr('вишненвые пирожки', 16, 13000, 'мощни сочни восточни',
#                 'https://kfs-menu.ru/images/menu/pirozhok-s-vishney.cu4mbcwvutf5np63seyme9owld9n')
# database.add_pr('рожок', 17, 25000, 'мощни сочни восточни',
#                 'https://kfs-menu.ru/images/menu/morozhenoe-rozhok-letnee.jpg')
# database.add_pr('твистер', 18, 25000, 'мощни сочни восточни',
#                 'https://i.otzovik.com/objects/b/1650000/1640212.png')
#

bot = telebot.TeleBot(config.bot_token)
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# обработка команды старт


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    # полувчить теграмм айди
    user_id = message.from_user.id
    # проверка пользователя
    checker = database.check_user(user_id)
    #  если юзер есть в базе
    if checker:
        # получим актульный список продуктов
        products = database.get_pr_name_id()
        # отправим сообщение с меню\
        bot.send_message(user_id, ' выберите пункт меню', reply_markup=butt.main_menu_kb(products))
    elif not checker:
        bot.send_message(user_id, ' привет\nотправь имя')
        bot.register_next_step_handler(message, get_name)
        #  переход на этап получения имени(дз)


def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'отлично, я тебя запомнил', reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, 'а теперь отправь свой номер', reply_markup=butt.phone_number_kb())
    bot.register_next_step_handler(message, get_number, name)


def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        # созраним контакт
        phone_number = message.contact.phone_number
        # сохраняем его в базе
        database.register_user(user_id, name, phone_number, 'Not yet')
        # торываем меню
        products = database.get_pr_name_id()
        bot.send_message(user_id, 'регистрация завершена', reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'выберите пункт меню', reply_markup=butt.main_menu_kb(products))
    elif not message.contact:
        bot.send_message(user_id, 'отправьте свой номер используя кнопку!', reply_markup=butt.phone_number_kb())
        bot.register_next_step_handler(message, get_number, name)
    # вызов data_base.register_user(user_id, name , phone_number, "not yet")
    # bot.send_message(user_id, 'menu',reply_markup=butt.main_menu(products)

# обработчик выбора количества


@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'add_to_cart', 'back', 'a'])
def get_user_product_count(call):
    # сохраняем айди юзера
    user_id = call.message.chat.id
    message_id = call.message.message_id
    # оесли пользователь нажал +
    if call.data == 'increment':
        actual_count = users[user_id]['pr_count']
        users[user_id]['pr_count'] += 1
        # меняем значение счетчика
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=butt.choose_product_count('increment', actual_count))
    elif call.data == 'decrement':
        users[user_id]['pr_count'] -= 1
        actual_count = users[user_id]['pr_count']

        # меняем значение счетчика
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=butt.choose_product_count('decrement', actual_count))
    elif call.data == 'back':
        products = database.get_pr_name_id()
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'выберите пункт меню:',
                         reply_markup=butt.main_menu_kb(products))
    elif call.data == 'add_to_cart':
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']

        database.add_pr_to_kor(user_id, user_product, product_count)

        product = database.get_pr_name_id()
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, 'продукт был добавлен в корзину \nчто-нибудь еще?',
                         reply_markup=butt.main_menu_kb(product))


# обработчик кнопок оформить заказ и корзина


@bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'next', 'page_bef', 'al', 'delete']
                            or call.data.startswith('❌'))
def main_menu_hadle(call):
    user_id = call.message.chat.id
    # сохраним айди сообщения
    message_id = call.message.message_id
    # если нажал на кнопку : оформить заказ
    if call.data == 'order':
        # удаление сообщение с инлайн кнопками
        bot.delete_message(user_id, message_id)
        # поменяем текст на "отправьте "
        bot.send_message(user_id, 'отправьте локацию', reply_markup=butt.loc_kb())
        bot.register_next_step_handler(call.message, get_location)
    elif call.data == 'cart':
        user_id = call.message.chat.id
        # сохраним айди сообщения
        user_cart = database.get_exact_user_kor(user_id)
        print(user_cart)
        total_ammount = 0
        full_text = 'ваша корзина:\n\n'

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}сум\n\n'
            total_ammount += i[2]
            # итог
        full_text += f"итог: {total_ammount}\n"
        bot.edit_message_text(full_text, user_id, message_id, reply_markup=butt.delete_from_cart())
    elif call.data == 'next':
        products = database.get_pr_name_id()
        bot.edit_message_text('следующая страница:\nвыберите пункт меню:', user_id, message_id,
                              reply_markup=butt.next_page(products))
    elif call.data == 'page_bef':
        products = database.get_pr_name_id()
        bot.edit_message_text('предыдущая страница:\nвыберите пункт меню:', user_id, message_id,
                              reply_markup=butt.main_menu_kb(products))
    elif call.data == 'al':
        database.delete_all_pr_from_cart(user_id)
        products = database.get_pr_name_id()
        bot.edit_message_text('козина очищена\nвыберите пункт меню:', user_id, message_id,
                              reply_markup=butt.main_menu_kb(products))
    elif call.data == 'delete':
        products = database.get_exact_user_kor(user_id)
        bot.edit_message_text('выберите продукт', user_id, message_id, reply_markup=butt.delete_menu_kb(products))
    elif '❌' in call.data:
        products = database.get_pr_name_id()
        database.delete_exact_pr_from_cart(pr_id=int(call.data[1:]), kr_id=user_id)
        bot.edit_message_text('вы успешно удалили продукт из корзины\nвыберите пункт меню:', user_id,
                              message_id, reply_markup=butt.main_menu_kb(products))


def get_location(message):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        # сохранить переменные координаты
        longitude = message.location.longitude
        # преобразуем координтаы в норм адресс
        address = geolocator.reverse((latitude, longitude)).address
        # запрос потверждения
        # получим корзину юзера
        user_cart = database.get_exact_user_kor(user_id)
        # формируем сообщение со всеми данными
        total_ammount = 0
        full_text = 'ваш заказ:\n\n'
        user_info = database.get_user_num_name(user_id)
        full_text += f"имя:{user_info[0]}\nномер телефона: {user_info[1]}\n\n"
        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}сум\n\n'
            total_ammount += i[2]
            # итог и адрес
        full_text += f"итог: {total_ammount}\n\nадресс: {address}"
        bot.send_message(user_id, full_text, reply_markup=butt.get_accept_kb())
        # переход на этап потверждения
        bot.register_next_step_handler(message, get_accept, address, full_text)


def get_accept(message, address, full_text):
    user_id = message.from_user.id
    products = database.get_pr_name_id()
    user_cart = database.get_exact_user_kor(user_id)
    print(user_cart)
    if message.text == 'потвердить':
        # после потвердения заказа очищаем корзину
        database.delete_all_pr_from_cart(user_id)
        bot.send_message(-1001982414088, full_text.replace('ваш', "новый"))
        bot.send_message(user_id, f'вы потвердили заказ на адрес:\n\n{address}',
                         reply_markup=ReplyKeyboardRemove())
        # text = f"покупка товара: {user_cart[0][0]}\n" f"Количетсво: {user_cart[0][1]}"
        total_ammount = 0
        full_text = 'ваш заказ:\n\n'
        for i in user_cart:
            full_text += f'{i[0]} x кол:{i[1]} = {i[2]}сум\n\n'
            total_ammount += i[2]

        bot.send_invoice(message.chat.id, 'покупка продуктов', full_text, "invoice", config.pay_token, 'UZS',
                         [types.LabeledPrice('С вас:', 100 * int(total_ammount))])
        print(user_cart[0])
    elif message.text == 'отменить':
        bot.send_message(user_id, 'вы отменили заказ',
                         reply_markup=ReplyKeyboardRemove())
    bot.send_message(user_id, 'меню:', reply_markup=butt.main_menu_kb(products))


@bot.callback_query_handler(lambda call: call.data.isdigit() in database.get_pr_id())
def get_user_pr(call):
    # сохранним айди
    user_id = call.message.chat.id
    # сохраним айди сообщения
    message_id = call.message.message_id
    product = database.get_exact_product(call.data)
    print(product)
    # сохраним продукт во временный словарь(call data - значение нажатой кнопки(inline))
    users[user_id] = {'pr_name': call.data, 'pr_count': 1}
    file = product[0]
    # поменять кнопки на выбор количсетва
    bot.delete_message(user_id, message_id)
    bot.send_photo(user_id, file, f'описание: {product[1]}\nцена: {product[2]}\n\nвыберите количество',
                   reply_markup=butt.choose_product_count())
    # products = data_base.get_pr_name_id()
    # bot.edit_message_text('выберите пункт меню:', user_id, message_id, reply_markup=butt.main_menu_kb(products))


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Оплата не прошла - попробуйте, пожалуйста, еще раз,"
                                                "или свяжитесь с администратором бота.")


# при корректной оплате
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):

    # здесь подключение к базе данных и внесение данных в таблицу
    bot.send_message(message.chat.id, 'Ваш заказ был успешным')


bot.polling(non_stop=True)
