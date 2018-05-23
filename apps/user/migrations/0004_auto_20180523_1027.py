# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-23 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='follow',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
