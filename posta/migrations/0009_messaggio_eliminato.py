# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-05-13 11:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posta', '0008_destinatario_invalido'),
    ]

    operations = [
        migrations.AddField(
            model_name='messaggio',
            name='eliminato',
            field=models.BooleanField(default=False),
        ),
    ]