# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Seminar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords_string', models.CharField(max_length=500, editable=False, blank=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('_meta_title', models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('status', models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True)),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True)),
                ('short_url', models.URLField(null=True, blank=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('featured_image', mezzanine.core.fields.FileField(max_length=255, verbose_name='Featured image', blank=True)),
                ('featured', models.BooleanField(default=False, help_text='Highlight this item above others', verbose_name='Featured')),
                ('length', models.PositiveIntegerField(help_text='Seminar duration in minutes', null=True, verbose_name='Length', blank=True)),
                ('price', models.DecimalField(default=0, verbose_name='Price', max_digits=8, decimal_places=2)),
                ('preview_video_link', models.URLField(help_text='Publicly-accessible teaser or preview', verbose_name='Preview Video Link', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ['-featured', '-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='SeminarContentArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('video_link', models.URLField(verbose_name='Video Link', blank=True)),
                ('seminar', models.ForeignKey(related_name='content_areas', to='mezzanine_seminars.Seminar')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'content area',
                'verbose_name_plural': 'content areas',
            },
        ),
        migrations.CreateModel(
            name='SeminarRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('price', models.DecimalField(default=0, verbose_name='Price', max_digits=8, decimal_places=2)),
                ('payment_method', models.CharField(max_length=100, verbose_name='Payment method')),
                ('transaction_id', models.CharField(max_length=100, verbose_name='Transaction ID', blank=True)),
                ('transaction_notes', models.TextField(verbose_name='Transaction notes', blank=True)),
                ('purchaser', models.ForeignKey(related_name='seminar_registrations', to=settings.AUTH_USER_MODEL)),
                ('seminar', models.ForeignKey(related_name='registrations', to='mezzanine_seminars.Seminar')),
            ],
        ),
        migrations.CreateModel(
            name='SeminarSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('field_type', models.IntegerField(verbose_name='Question type', choices=[(1, 'Rating'), (2, 'Text')])),
                ('prompt', models.CharField(max_length=300, verbose_name='Prompt')),
                ('required', models.BooleanField(default=True, verbose_name='Required')),
                ('seminar', models.ForeignKey(related_name='survey_questions', to='mezzanine_seminars.Seminar')),
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
            model_name='seminar',
            name='subjects',
            field=models.ManyToManyField(related_name='seminars', to='mezzanine_seminars.SeminarSubject', blank=True),
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
        migrations.AlterUniqueTogether(
            name='seminarregistration',
            unique_together=set([('purchaser', 'seminar')]),
        ),
    ]
