# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-06-21 12:30
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donazioni', '0007_auto_20170617_1433'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='etichetta',
            options={'ordering': ['slug'], 'permissions': (('view_etichetta', 'Can view etichetta'),), 'verbose_name': 'Etichetta', 'verbose_name_plural': 'Etichette'},
        ),
        migrations.AlterField(
            model_name='donazione',
            name='importo',
            field=models.FloatField(default=0.0, help_text='Importo in EUR della donazione', validators=[django.core.validators.MinValueValidator(0.01, "L'importo della donazione è al disotto del minimo consentito")], verbose_name='Importo in EUR'),
        ),
    ]
