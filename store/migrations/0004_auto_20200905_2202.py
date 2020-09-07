# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200905_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_number',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
