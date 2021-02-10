# Сравнилка цен на книги в РБ с API
##### Проект представляет из себя сервис, который дает возможность сравнить цены и выбрать выгодный для себя вариант покупки книги. 
##### Он включает себя: 
- Веб-сайт
- TelegramBot
- API

![alt tag](https://i.ibb.co/Y0P5Ssg/Sravnilka.png)

## Веб-сайт

![alt tag](https://i.ibb.co/4jMQFWk/Peek-2021-02-08-15-32.gif)

## TelegramBot + API

![alt tag](https://i.ibb.co/0nt1fcP/Peek-2021-02-08-15-43.gif)
===========
![alt tag](https://i.ibb.co/2NFh5GJ/logo.png)

[Django-Q](https://django-q.readthedocs.io/en/latest/) - это встроенная очередь задач Django. Она интегрируется в Админ панель, откуда ей очень удобно управлять.
В планировщик передается функция, которую нужно вызывать в запланированное время и с определенной периодичностью, а так же словарь с xpath для парсинга данных с интернет-магазинов.

## Пример работы с API

##### Запрос :
```python
from requests_html import HTMLSession
from pprint import pprint


def resp(link):
    """Функция делает запрос на API и парсит json"""
    with HTMLSession() as session:
        list_json = session.get(link).json()['results']
    return list_json


url = 'http://127.0.0.1:8000/api/?search=Сталкер'
pprint(resp(url))
```
##### Ответ :
```
[{'author': 'Андрей Левицкий, Алексей Бобл, 2020',
  'id': 23537,
  'link': 'https://oz.by/books/more10295808.html',
  'price': 16.26,
  'shop': 'https://oz.by',
  'title': 'Я - сталкер. Осознание'},
 {'author': 'Нэнси Сталкер, 2020',
  'id': 25542,
  'link': 'https://oz.by/books/more10951889.html',
  'price': 40.44,
  'shop': 'https://oz.by',
  'title': 'Япония. История и культура'}]
```
