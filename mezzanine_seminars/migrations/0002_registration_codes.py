# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_seminars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50, verbose_name='Code')),
                ('available', models.PositiveIntegerField(help_text='This number will be updated automatically as users register', verbose_name='Available')),
                ('seminar', models.ForeignKey(related_name='registration_codes', to='mezzanine_seminars.Seminar')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='registrationcode',
            unique_together=set([('seminar', 'code')]),
        ),
    ]
