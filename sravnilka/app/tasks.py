from django_q.tasks import schedule
import asyncio
import aiohttp
from lxml import html
from .models import Books
import re


async def cor(url, sem, dictt):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html_code = await resp.text()
        dom_tree = html.fromstring(html_code)
        of_link = dictt['of_link']
        title = dom_tree.xpath(dictt['title'])
        author = dom_tree.xpath(dictt['author'])
        link = dom_tree.xpath(dictt['link'])
        img = dom_tree.xpath(dictt['img'])
        price = dom_tree.xpath(dictt['price'])
        for t, a, l, i, p in zip(title, author, link, img, price):
            p = float(str('.'.join(re.findall('(\d+)', p.text))))
            if 'http' not in l:
                l = of_link + l
            if 'http' not in i:
                i = of_link + i
            try:
                Books(shop=of_link, title=t.text, author=a.text, link=l, img_link=i, price=p).save()
            except Exception:
                continue


async def main(urll, quantity, dictt):
    urls = []
    for i in range(1, (quantity + 1)):
        urls.append(f'{urll}{i}')
    tasks = []
    sem = asyncio.Semaphore(value=5)
    for url in urls:
        task = asyncio.Task(cor(url, sem, dictt))
        tasks.append(task)
    await asyncio.gather(*tasks)


def start(q, dictt):
    Books.objects.all().delete()
    for urll, d in dictt.items():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(urll, q, d))


def www():
    Books.objects.all().delete()