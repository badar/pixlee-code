# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0007_remove_picture_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
    ]
