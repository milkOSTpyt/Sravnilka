from django.db import models

class Books(models.Model):
    ''' База книг '''
    title = models.CharField('Название', max_length=250)
    author = models.CharField('Автор', max_length=150, default='Не указан')
    link = models.CharField('Название', max_length=250, unique=True)
    img_link = models.CharField('Название', max_length=250)
    price = models.FloatField('Цена', default=0)