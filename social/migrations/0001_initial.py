# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('anagrafica', '0002_auto_20160116_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('ultima_modifica', models.DateTimeField(db_index=True, auto_now=True)),
                ('commento', models.TextField(verbose_name='Testo del commento')),
                ('oggetto_id', models.PositiveIntegerField(db_index=True)),
                ('autore', models.ForeignKey(related_name='commenti', to='anagrafica.Persona')),
                ('oggetto_tipo', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Commenti',
            },
        ),
        migrations.CreateModel(
            name='Giudizio',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('creazione', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('ultima_modifica', models.DateTimeField(db_index=True, auto_now=True)),
                ('positivo', models.BooleanField(db_index=True, default=True, verbose_name='Positivo')),
                ('oggetto_id', models.PositiveIntegerField(db_index=True)),
                ('autore', models.ForeignKey(related_name='giudizi', to='anagrafica.Persona')),
                ('oggetto_tipo', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Giudizi',
            },
        ),
    ]
