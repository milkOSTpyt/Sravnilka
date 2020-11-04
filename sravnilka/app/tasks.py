from django_q.tasks import schedule
import asyncio
import aiohttp
from lxml import html
from .models import Books
import re


async def cor(url, sem):
    async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html_code = await resp.text()
        dom_tree = html.fromstring(html_code)
        of_link = 'biblio.by'
        title = dom_tree.xpath('//div[@class="product-name"]/a')
        author = dom_tree.xpath('//p[@class="author"]')
        link = dom_tree.xpath('//div[@class="product-name"]/a//@href')
        img = dom_tree.xpath('//div[@class="images-container"]//img/@src')
        price = dom_tree.xpath('//p[@class="special-price"]//span[@class="price"] | //span[@class="regular-price"]//span[@class="price"]')
        for t, a, l, i, p in zip(title, author, link, img, price):
            p = float(str('.'.join(re.findall('(\d+)', p.text))))
            print(p, type(p))
            Books(shop=of_link, title=t.text, author=a.text, link=l, img_link=i, price=p).save()


async def main(url, quantity):
    urls = []
    for i in range(1, (quantity + 1)):
        urls.append(f'{url}{i}')
    tasks = []
    sem = asyncio.Semaphore(value=3)
    for url in urls:
        task = asyncio.Task(cor(url, sem))
        tasks.append(task)
    await asyncio.gather(*tasks)


def start(url, q):
    Books.objects.all().delete()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url, q))