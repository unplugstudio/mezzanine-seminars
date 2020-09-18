# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mezzanine_seminars', '0004_auto_20200916_1713'),
    ]

    operations = [
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
            ],
        ),
        migrations.AlterModelOptions(
            name='seminar',
            options={'ordering': ['-featured', '-publish_date']},
        ),
        migrations.AddField(
            model_name='seminarregistration',
            name='seminar',
            field=models.ForeignKey(related_name='registrations', to='mezzanine_seminars.Seminar'),
        ),
        migrations.AlterUniqueTogether(
            name='seminarregistration',
            unique_together=set([('purchaser', 'seminar')]),
        ),
    ]
