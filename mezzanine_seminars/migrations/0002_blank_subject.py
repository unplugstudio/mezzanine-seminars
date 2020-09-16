# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_seminars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='subjects',
            field=models.ManyToManyField(related_name='seminars', to='mezzanine_seminars.SeminarSubject', blank=True),
        ),
    ]
