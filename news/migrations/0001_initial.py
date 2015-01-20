# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp')),
            ],
            options={
                'ordering': ('-timestamp',),
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
    ]
