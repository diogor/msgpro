# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20160728_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='identidade',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]