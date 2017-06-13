# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-06-13 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donazioni', '0002_etichetta_default'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donatore',
            options={'permissions': (('view_donatore', 'Can view donatore'),), 'verbose_name': 'Donatore', 'verbose_name_plural': 'Donatori'},
        ),
        migrations.AlterModelOptions(
            name='donazione',
            options={'permissions': (('view_donazione', 'Can view donazione'),), 'verbose_name': 'Donazione', 'verbose_name_plural': 'Donazioni'},
        ),
    ]