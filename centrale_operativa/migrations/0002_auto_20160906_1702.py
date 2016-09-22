# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-06 17:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('centrale_operativa', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reperibilita',
            options={'ordering': ['-inizio', '-fine'], 'permissions': (('view_reperibilita', 'Can view Reperibilità'),), 'verbose_name': 'Reperibilità', 'verbose_name_plural': 'Reperibilità'},
        ),
        migrations.AlterModelOptions(
            name='turno',
            options={'permissions': (('view_turno', 'Can view Turno'),), 'verbose_name': 'Turno', 'verbose_name_plural': 'Turni'},
        ),
    ]