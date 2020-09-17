# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_seminars', '0003_auto_20200916_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminar',
            name='featured',
            field=models.BooleanField(default=False, help_text='Highlight this item above others', verbose_name='Featured'),
        ),
        migrations.AddField(
            model_name='seminar',
            name='featured_image',
            field=mezzanine.core.fields.FileField(max_length=255, verbose_name='Featured image', blank=True),
        ),
    ]
