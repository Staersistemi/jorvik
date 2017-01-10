# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-18 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20160606_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autorizzazione',
            name='destinatario_ruolo',
            field=models.CharField(choices=[('PRES', 'Presidenza'), ('US-GEN', 'Gestione dei Soci'), ('US-TRASF', 'Gestione dei Trasferimenti'), ('US-EST', 'Gestione delle Estensioni'), ('US-FOT', 'Gestione delle Fototessere'), ('US-TIT', 'Gestione dei Titoli nella Sede'), ('US-RIS', 'Gestione delle Riserve'), ('ATT-PART', "Gestione dei Partecipanti all'Attività"), ('CB-PART', 'Gestione dei Partecipanti al Corso Base'), ('US-APP', 'Gestione degli Appartenenti alla Sede'), ('SA-SAN', 'Gestione delle Donazioni Sangue'), ('ASP', 'Autogestione Aspirante')], db_index=True, max_length=16),
        ),
    ]