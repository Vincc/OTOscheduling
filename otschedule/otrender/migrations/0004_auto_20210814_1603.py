# Generated by Django 3.2.6 on 2021-08-14 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otrender', '0003_auto_20210813_1836'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessiondates',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='sessiontimes',
            options={'ordering': ['time']},
        ),
    ]
