# Generated by Django 3.2.9 on 2021-11-30 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='total',
        ),
    ]
