from django.db import models

class Books(models.Model):
    ''' База книг '''
    shop = models.CharField('Магазин', max_length=150)
    title = models.CharField('Название книги', max_length=250)
    author = models.CharField('Автор', max_length=150, null=True, blank=True)
    link = models.CharField('Ссылка на товар', max_length=250, unique=True)
    img_link = models.CharField('Ссылка на картинку', max_length=250)
    price = models.FloatField('Цена', null=True, blank=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"