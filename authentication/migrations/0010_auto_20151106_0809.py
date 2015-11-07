# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0009_auto_20151106_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotifications',
            name='userfrom',
            field=models.ForeignKey(related_name='notif_from', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usernotifications',
            name='user',
            field=models.ForeignKey(related_name='notif_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
