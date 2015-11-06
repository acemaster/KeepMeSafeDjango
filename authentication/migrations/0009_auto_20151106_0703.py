# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_usernotifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotifications',
            name='read',
            field=models.IntegerField(default=0),
        ),
    ]
