# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0012_auto_20150821_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='task',
            field=models.ForeignKey(to='connector.Task'),
        ),
    ]
