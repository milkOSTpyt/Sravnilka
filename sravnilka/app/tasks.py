from django.db.utils import IntegrityError
import asyncio
import aiohttp
from lxml import html
from .models import Books
import re

list_503 = []


def parser(html_code, dict_xpath):
    """ С помщью библиотеки lxml мы получаем дом дерево и достаем оттуда наши 
    данные. Далее записываем их в базу """
    dom_tree = html.fromstring(html_code)
    of_link = dict_xpath['of_link']
    title = dom_tree.xpath(dict_xpath['title'])
    author = dom_tree.xpath(dict_xpath['author'])
    link = dom_tree.xpath(dict_xpath['link'])
    img = dom_tree.xpath(dict_xpath['img'])
    price = dom_tree.xpath(dict_xpath['price'])
    for t, a, l, i, p in zip(title, author, link, img, price):
        if p.text == 'Уведомить о появлении':
            continue
        if 'http' not in l:
            l = of_link + l
        if 'http' not in i:
            i = of_link + i
        try:
            #Здесь мы избавляемся от лишних пробелов в цене, и оставляем только цифры для преобразовыввания цены в float
            p=float(str('.'.join(re.findall('(\d+)',re.sub('[\s]','',p.text)))))
            Books.objects.get_or_create(shop=of_link, title=t.text, 
                                    author=a.text, link=l, img_link=i, price=p)
        except Exception as e:
            print(f'{e} - {t.text} {l}')
            continue


async def get_html(link, sem, dict_xpath):
    """ Устанавливаем Semaphore. 
    Получаем response и передаем html код функции parser """
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                print(f'{link}, {resp.status}')
                if resp.status == 503:
                    list_503.append(link)
                html_code = await resp.text()
                parser(html_code, dict_xpath)


async def collect_tasks(url, dict_xpath):
    """ Здесь мы создаем список урлов для парсинга и закидываем наши задачи в 
    gather. Так же настраиваем Semaphore для ограничения количества запросов.
    В конце мы проверяем список урлов, которые небыли выполнены и закидываем их 
    еще раз в gather """
    urls = []
    for i in range(1, (dict_xpath['pages'] + 1)):
        urls.append(f'{url}{i}')
    tasks = []
    sem = asyncio.Semaphore(dict_xpath['sem'])
    for link in urls:
        task = asyncio.Task(get_html(link, sem, dict_xpath))
        tasks.append(task)
    await asyncio.gather(*tasks)
    tasks_503 = []
    while list_503:
        for url_503 in list_503:
            task_503 = asyncio.Task(get_html(url_503, sem, dict_xpath))
            tasks_503.append(task_503)
            list_503.remove(url_503)
        await asyncio.gather(*tasks_503)


def start(data):
    """ Функция, которая запускается из Django админки(Django-q).Сюда 
    передается словарь с данными для парсинга """
    Books.objects.all().delete()
    for url, dict_xpath in data.items():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(collect_tasks(url, dict_xpath))


def www():
    """ Временная функция для удаления базы """
    Books.objects.all().delete()