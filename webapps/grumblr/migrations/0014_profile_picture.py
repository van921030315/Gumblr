# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0013_auto_20171005_0557'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, upload_to='user-img'),
        ),
    ]