# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userlocation_usermessages_usersafetylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermessages',
            name='userfrom',
            field=models.OneToOneField(related_name='message_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermessages',
            name='userto',
            field=models.OneToOneField(related_name='message_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usersafetylist',
            name='userfrom',
            field=models.OneToOneField(related_name='List_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usersafetylist',
            name='userto',
            field=models.OneToOneField(related_name='List_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
