# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0002_userprofile_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.CharField(max_length=100)),
                ('longt', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMessages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('messages', models.CharField(max_length=1000)),
                ('message_data', models.DateField(auto_now=True)),
                ('userfrom', models.ForeignKey(related_name='message_from', to=settings.AUTH_USER_MODEL, unique=True)),
                ('userto', models.ForeignKey(related_name='message_to', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSafetyList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField()),
                ('userfrom', models.ForeignKey(related_name='List_from', to=settings.AUTH_USER_MODEL, unique=True)),
                ('userto', models.ForeignKey(related_name='List_to', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
