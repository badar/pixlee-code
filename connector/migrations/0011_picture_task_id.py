# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0010_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='task_id',
            field=models.ForeignKey(to='connector.Task', default=0),
        ),
    ]
