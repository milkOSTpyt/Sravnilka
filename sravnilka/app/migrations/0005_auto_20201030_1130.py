# Generated by Django 2.2 on 2020-10-30 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201030_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='price',
            field=models.CharField(default='0', max_length=50, verbose_name='Цена'),
        ),
    ]