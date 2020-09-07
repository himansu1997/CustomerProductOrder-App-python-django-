# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=250, null=True, blank=True)),
                ('last_name', models.CharField(max_length=250, null=True, blank=True)),
                ('email_id', models.CharField(max_length=250, null=True, blank=True)),
                ('mobile_number', models.CharField(max_length=250, null=True, blank=True)),
                ('address', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'customer_details',
                'verbose_name_plural': 'customer_details',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('billing_address', models.CharField(max_length=250)),
                ('shipping_address', models.CharField(max_length=250)),
                ('status', models.BooleanField(default=True)),
                ('order_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('order_amount', models.DecimalField(default=0.0, max_digits=15, decimal_places=2)),
                ('order_id', models.ForeignKey(to='store.Customer')),
            ],
            options={
                'verbose_name': 'order_details',
                'verbose_name_plural': 'order_details',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_number', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=250)),
                ('brand', models.CharField(max_length=250, blank=True)),
                ('shipping', models.CharField(max_length=250, blank=True)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(default=0.0, max_digits=15, decimal_places=2)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'product_details',
                'verbose_name_plural': 'product_details',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='product',
            field=models.ForeignKey(to='store.Product'),
        ),
    ]
