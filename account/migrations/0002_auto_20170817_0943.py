# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, null=True, unique=True, verbose_name='注册邮箱'),
        ),
    ]
