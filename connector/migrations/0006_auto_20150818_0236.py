# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0005_auto_20150818_0231'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='state',
            new_name='status',
        ),
    ]
