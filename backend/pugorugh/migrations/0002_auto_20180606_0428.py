# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-06 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(help_text='status; Enter, (l) Liked, (d) Disliked, (u) Undecided', max_length=1),
        ),
    ]
