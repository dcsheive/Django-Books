# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-18 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_user_user_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(default="I'm a new user :)"),
            preserve_default=False,
        ),
    ]
