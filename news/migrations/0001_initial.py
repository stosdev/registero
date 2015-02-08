# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Tytu\u0142')),
                ('content', models.TextField(verbose_name='Zawarto\u015b\u0107')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Czas dodania')),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'ordering': ('-timestamp',),
                'verbose_name': 'Aktualno\u015b\u0107',
                'verbose_name_plural': 'Aktualno\u015bci',
            },
            bases=(models.Model,),
        ),
    ]
