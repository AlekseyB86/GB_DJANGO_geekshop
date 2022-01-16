# Generated by Django 3.2.9 on 2022-01-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0002_order_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('FM', 'формирование'), ('STP', 'передан в обработку'), ('DLV', 'доставка'), ('DN', 'выдан'), ('CNC', 'отменен')], default='FM', max_length=3),
        ),
    ]