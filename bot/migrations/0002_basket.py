# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2021-04-22 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('user_id', models.IntegerField(help_text='Saves persons user_id', primary_key=True, serialize=False)),
                ('products', models.CharField(help_text='Day and time when buyer will receive his order', max_length=200)),
                ('date', models.DateTimeField(auto_now=True, help_text='Saves time of last message from this user')),
            ],
        ),
    ]