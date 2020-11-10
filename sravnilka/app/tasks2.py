from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from django_q.tasks import schedule
from django.db import IntegrityError
from .models import Books
import re


def qwe(q):
    def pars_bestbooks(url):
        ''' Парсер забирает данные с сайта bestbooks.by . Он работает многопоточно. '''
        with HTMLSession() as session:
            resp = session.get(url)
        of_link = 'https://bestbooks.by'
        title = resp.html.xpath('//*[@class="ok-product__title-cont"]//a')
        link = resp.html.xpath('//div[@class="ok-product__img"]//@href')
        img = resp.html.xpath('//div[@class="ok-product__img"]//@src')
        price = resp.html.xpath('//span[@class="ok-product__price-main"]')
        list_bestbooks = []
        for t, l, i, p in zip(title, link, img, price):
            if 'http' not in l:
                l = of_link + l
            if 'http' not in i:
                i = of_link + i
            try:
                p = float(str('.'.join(re.findall('(\d+)', p.text))))
                print(f'{t.text}, {p}')
                Books(shop=of_link, title=t.text, link=l, img_link=i, price=p).save()
            except IntegrityError:
                continue
            except ValueError:
                continue


    list1 = []
    for i in range(q):
        list1.append(f'https://bestbooks.by/find/?page_id={i}')

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(pars_bestbooks, list1)


def qwe2(q):
    def pars_bestbooks(url):
        ''' Парсер забирает данные с сайта bestbooks.by . Он работает многопоточно. '''
        with HTMLSession() as session:
            resp = session.get(url)
        of_link = 'https://booklover.by'
        title = resp.html.xpath('//*[@class="descr_holder"]//span[@class="text"]')
        author = resp.html.xpath('//*[@class="descr_holder"]//span[@class="title"]')
        link = resp.html.xpath('//*[@class="item munit"]/a[1]/@href')
        img = resp.html.xpath('//*[@class="item munit"]//@src')
        price = resp.html.xpath('//*[@class="price"] | //*[@class="basket txc_dark_grey"]')
        list_bestbooks = []
        for t, a, l, i, p in zip(title, author, link, img, price):
            if 'http' not in l:
                l = of_link + l
            if 'http' not in i:
                i = of_link + i
            try:
                p = float(str('.'.join(re.findall('(\d+)', p.text))))
                print(f'{t.text}, {p}')
                Books(shop=of_link, title=t.text, author=a.text, link=l, img_link=i, price=p).save()
            except IntegrityError:
                continue
            except ValueError:
                continue


    list1 = []
    for i in range(q):
        list1.append(f'https://booklover.by/catalog/?PAGEN_1={i}')

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(pars_bestbooks, list1)