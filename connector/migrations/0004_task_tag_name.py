# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0003_auto_20150817_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tag_name',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
