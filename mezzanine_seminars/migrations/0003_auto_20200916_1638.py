# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_seminars', '0002_blank_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seminarcontentarea',
            options={'ordering': ('_order',), 'verbose_name': 'content area', 'verbose_name_plural': 'content areas'},
        ),
        migrations.RenameField(
            model_name='seminar',
            old_name='public_video_link',
            new_name='preview_video_link',
        ),
        migrations.RemoveField(
            model_name='seminar',
            name='private_content',
        ),
        migrations.RemoveField(
            model_name='seminar',
            name='private_video_link',
        ),
        migrations.AddField(
            model_name='seminarcontentarea',
            name='video_link',
            field=models.URLField(verbose_name='Video Link', blank=True),
        ),
    ]
