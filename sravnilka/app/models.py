from django.db import models

class Books(models.Model):
    ''' База книг '''
    shop = models.CharField('Магазин', max_length=100)
    title = models.CharField('Название книги', max_length=255)
    author = models.CharField('Автор', max_length=255, null=True, blank=True)
    link = models.CharField('Ссылка на товар', max_length=255, unique=True)
    img_link = models.CharField('Ссылка на картинку', max_length=255)
    price = models.FloatField('Цена', null=True, blank=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['price']