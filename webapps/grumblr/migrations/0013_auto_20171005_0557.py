# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0012_auto_20171005_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=420, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='firstname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lastname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]