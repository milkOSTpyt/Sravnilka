from django.db.utils import IntegrityError
from fake_useragent import UserAgent
import asyncio
import aiohttp
from lxml import html
from .models import Books
import re


ua = UserAgent()

list_errors = []


def parser(url, html_code, dict_xpath):
    """ С помщью библиотеки lxml мы получаем дом дерево и достаем оттуда наши 
    данные. Далее записываем их в базу """
    dom_tree = html.fromstring(html_code)
    title = dom_tree.xpath(dict_xpath['title'])
    author = dom_tree.xpath(dict_xpath['author'])
    link = dom_tree.xpath(dict_xpath['link'])
    img = dom_tree.xpath(dict_xpath['img'])
    price = dom_tree.xpath(dict_xpath['price'])
    for t, a, l, i, p in zip(title, author, link, img, price):
        if p.text == 'Уведомить о появлении':
            continue
        if 'http' not in l:
            l = url + l
        if 'http' not in i:
            i = url + i
        try:
            p=float(str('.'.join(re.findall('(\d+)',re.sub('[\s]','',p.text)))))
            Books.objects.get_or_create(shop=url, title=t.text, author=a.text, link=l, img_link=i, price=p)
        except Exception as e:
            print(f'{e} - {l}')
            continue


async def get_html(url, link, sem, dict_xpath):
    """ Устанавливаем Semaphore. 
    Получаем response и передаем html код функции parser """
    headers = {'User-Agent': ua.random,}
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=headers) as resp:
                print(f'{link}, {resp.status}')
                if resp.status != 200:
                    list_errors.append(link)
                html_code = await resp.text()
                parser(url, html_code, dict_xpath)


async def error_links(url, sem, dict_xpath):
    """ Функция обрабатывает повторно ссылки, в которых произошли ошибки """
    tasks_errors = []
    while list_errors:
        for url_error in list_errors:
            task_errors = asyncio.Task(get_html(url,url_error, sem, dict_xpath))
            tasks_errors.append(task_errors)
            list_errors.remove(url_error)
        await asyncio.gather(*tasks_errors)


async def collect_tasks(url, dict_xpath):
    """ Здесь мы создаем список урлов для парсинга и закидываем наши задачи в 
    gather. Так же настраиваем Semaphore для ограничения количества запросов.
    В конце мы проверяем список урлов, которые небыли выполнены и закидываем их 
    еще раз в gather с помощью функции error_links """
    urls = []
    for link, quantity in dict_xpath['pages'].items():
        for i in range(1, quantity + 1):
            urls.append(f'{link}{i}')
    tasks = []
    sem = asyncio.Semaphore(dict_xpath['sem'])
    for link in urls:
        task = asyncio.Task(get_html(url, link, sem, dict_xpath))
        tasks.append(task)
    await asyncio.gather(*tasks)
    if list_errors:
        await error_links(url, sem, dict_xpath)


def start(data):
    """ Функция, которая запускается из Django админки(Django-q).Сюда 
    передается словарь с данными для парсинга. Так же функция удаляет старые данные из базы """
    for url, dict_xpath in data.items():
        Books.objects.filter(shop=url).delete()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(collect_tasks(url, dict_xpath))


def www():
    """ Временная функция для удаления базы """
    Books.objects.all().delete()