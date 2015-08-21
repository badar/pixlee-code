# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0011_picture_task_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='task_id',
            new_name='task',
        ),
    ]
