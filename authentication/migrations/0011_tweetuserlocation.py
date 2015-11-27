# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_auto_20151106_0809'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetUserLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('longt', models.CharField(max_length=100)),
            ],
        ),
    ]
