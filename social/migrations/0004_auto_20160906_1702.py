# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-06 17:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20160118_2059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commento',
            options={'permissions': (('view_commento', 'Can view commento'),), 'verbose_name_plural': 'Commenti'},
        ),
        migrations.AlterModelOptions(
            name='giudizio',
            options={'permissions': (('view_giudizio', 'Can view giudizio'),), 'verbose_name_plural': 'Giudizi'},
        ),
    ]
