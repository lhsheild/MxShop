# Generated by Django 2.2.1 on 2019-05-14 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190514_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': '购物车', 'verbose_name_plural': '购物车'},
        ),
    ]