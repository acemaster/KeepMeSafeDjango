# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20151105_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessages',
            name='userfrom',
            field=models.ForeignKey(related_name='message_from', to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='usermessages',
            name='userto',
            field=models.ForeignKey(related_name='message_to', to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='usersafetylist',
            name='userfrom',
            field=models.ForeignKey(related_name='List_from', to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='usersafetylist',
            name='userto',
            field=models.ForeignKey(related_name='List_to', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
