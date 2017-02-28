# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 20:31
from __future__ import unicode_literals

import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Tytu\u0142')),
                ('content', models.TextField(verbose_name='Zawarto\u015b\u0107')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Czas dodania')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site', verbose_name='Strona')),
            ],
            options={
                'ordering': ('-timestamp',),
                'verbose_name': 'Aktualno\u015bci',
                'verbose_name_plural': 'News',
            },
            managers=[
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
