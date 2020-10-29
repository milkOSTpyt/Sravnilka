# Generated by Django 2.2 on 2020-10-29 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('author', models.CharField(default='Не указан', max_length=150, verbose_name='Автор')),
                ('link', models.CharField(max_length=250, unique=True, verbose_name='Название')),
                ('img_link', models.CharField(max_length=250, verbose_name='Название')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
            ],
        ),
    ]
