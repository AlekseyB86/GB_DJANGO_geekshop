# Generated by Django 3.2.9 on 2022-01-14 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-created', 'is_active'), 'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
    ]
