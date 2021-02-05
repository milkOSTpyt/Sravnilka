import os
import telebot
from telebot import util
from telebot import types
from dotenv import load_dotenv
from requests_html import HTMLSession
load_dotenv()

bot = telebot.TeleBot(os.environ.get('TOKEN'))

markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=1)
btn_shop = types.KeyboardButton('Магазины 🏪')
btn_about = types.KeyboardButton('О нас 🕵🏻‍♂️')
markup.add(btn_shop, btn_about)


def resp(url):
    """Функция делает запрос на API и парсит json"""
    with HTMLSession() as session:
        list_json = session.get(url).json()['results']
    return list_json


def parse_data(msg):
    """Функция принимает сообщение пользователя и делает запрос на API,
    после чего возращает данные в виде строки, если они существуют в базе"""
    data = resp('http://127.0.0.1:8000/api/?search=' + msg)
    if data:
        string = ''
        for item in data:
            string += f'Название: {item["title"]}.\n' \
                      f'Магазин: {item["shop"]}.\n' \
                      f'Ссылка: {item["link"]}.\n' \
                      f'Цена: {item["price"]} Руб.\n' \
                      f'\n'
        return string
    else:
        return 'По вашему запросу ничего не найдено 🤷🏽‍♀️'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Ответ на служебные команды"""
    bot.reply_to(message, 'Введите название книги и мы предложим вам выгодные '
                          'варианты 😇', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def search(message):
    """Ответ на сообщения пользователя"""
    if message.text == markup.keyboard[0][0]['text']:
        bot.reply_to(message, '\n'.join(i['shop'] for i in resp(
                                          'http://127.0.0.1:8000/api/shops/')))
    elif message.text == markup.keyboard[0][1]['text']:
        bot.reply_to(message, 'С нами вы можете выгодно покупать любимые '
                              'книги. Просто введите название и мы соберем '
                              'для вас лучшие предложения 📚📖📔')
    else:
        str_msg = parse_data(message.text)
        if len(str_msg) > 12000:
            with open('sticker.webp', 'rb') as sticker:
                bot.send_sticker(message.chat.id, sticker)
        elif len(str_msg) > 4000:
            split_msg = util.split_string(str_msg, 4000)
            for text in split_msg:
                bot.reply_to(message, text)
        else:
            bot.reply_to(message, str_msg)


bot.polling()
