# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 20:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_auto_20170920_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intro',
            name='user',
        ),
        migrations.DeleteModel(
            name='Intro',
        ),
    ]
