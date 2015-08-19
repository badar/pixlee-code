# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0006_auto_20150818_0236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='name',
        ),
    ]
