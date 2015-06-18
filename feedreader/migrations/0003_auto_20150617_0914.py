# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedreader', '0002_entry_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='FisrtRevelant',
            field=models.ForeignKey(related_name='RevelantOne', to='feedreader.Entry', null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='SecondRevelant',
            field=models.ForeignKey(related_name='SecondRevelantTwo', to='feedreader.Entry', null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='ThirdRevelant',
            field=models.ForeignKey(related_name='RevelantThree', to='feedreader.Entry', null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='summary',
            field=models.TextField(null=True, blank=True),
        ),
    ]
