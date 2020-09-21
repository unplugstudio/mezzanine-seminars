# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_seminars', '0005_auto_20200918_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.PositiveSmallIntegerField(null=True, verbose_name='Rating', blank=True)),
                ('text_response', models.TextField(verbose_name='Text response', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('field_type', models.IntegerField(verbose_name='Question type', choices=[(1, 'Rating'), (2, 'Text')])),
                ('prompt', models.CharField(max_length=300, verbose_name='Prompt')),
                ('required', models.BooleanField(default=True, verbose_name='Required')),
                ('seminar', models.ForeignKey(related_name='questions', to='mezzanine_seminars.Seminar')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('registration', models.OneToOneField(related_name='survey_response', to='mezzanine_seminars.SeminarRegistration')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='question',
            field=models.ForeignKey(related_name='responses', to='mezzanine_seminars.SurveyQuestion'),
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='response',
            field=models.ForeignKey(related_name='responses', to='mezzanine_seminars.SurveyResponse'),
        ),
    ]
