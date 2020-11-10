from django_q.tasks import schedule
from django.db import IntegrityError
import asyncio
import aiohttp
from lxml import html
from .models import Books
import re

list_503 = []


async def cor(url, sem, dictt):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(f'{url}, {resp.status}')
                if resp.status == 503:
                    list_503.append(url)
                html_code = await resp.text()
            dom_tree = html.fromstring(html_code)
            of_link = dictt['of_link']
            title = dom_tree.xpath(dictt['title'])
            author = dom_tree.xpath(dictt['author'])
            link = dom_tree.xpath(dictt['link'])
            img = dom_tree.xpath(dictt['img'])
            price = dom_tree.xpath(dictt['price'])
            for t, a, l, i, p in zip(title, author, link, img, price):
                if p.text == 'Уведомить о появлении':
                    continue
                if 'http' not in l:
                    l = of_link + l
                if 'http' not in i:
                    i = of_link + i
                try:
                    p = float(str('.'.join(re.findall('(\d+)', p.text))))
                    Books(shop=of_link, title=t.text, author=a.text, link=l, 
                        img_link=i, price=p).save()
                except IntegrityError:
                    continue
                except ValueError:
                    continue


async def main(urll, dictt):
    urls = []
    for i in range(1, (dictt['pages'] + 1)):
        urls.append(f'{urll}{i}')
    tasks = []
    sem = asyncio.Semaphore(dictt['sem'])
    for url in urls:
        task = asyncio.Task(cor(url, sem, dictt))
        tasks.append(task)
    await asyncio.gather(*tasks)
    tasks_503 = []
    while list_503:
        for url_503 in list_503:
            task_503 = asyncio.Task(cor(url_503, sem, dictt))
            tasks_503.append(task_503)
            list_503.remove(url_503)
        await asyncio.gather(*tasks_503)


def start(dictt):
    Books.objects.all().delete()
    for urll, d in dictt.items():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(urll, d))


def www():
    Books.objects.all().delete()