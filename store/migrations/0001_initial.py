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
                ('customer_number', models.CharField(max_length=250, null=True, blank=True)),
                ('first_name', models.CharField(max_length=250, null=True, blank=True)),
                ('last_name', models.CharField(max_length=250, null=True, blank=True)),
                ('email_id', models.CharField(max_length=250, null=True, blank=True)),
                ('mobile_number', models.CharField(max_length=250, null=True, blank=True)),
                ('address', models.CharField(max_length=250, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_amount', models.DecimalField(default=0.0, max_digits=15, decimal_places=2)),
                ('order_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('oder_status', models.BooleanField(default=True)),
                ('billing_address', models.CharField(max_length=250)),
                ('shipping_address', models.CharField(max_length=250)),
                ('customer', models.ForeignKey(to='store.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Orderedproducts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.CharField(max_length=250, null=True, blank=True)),
                ('unit_price', models.DecimalField(default=0.0, max_digits=15, decimal_places=2)),
                ('price', models.DecimalField(default=0.0, max_digits=15, decimal_places=2)),
                ('order', models.ForeignKey(to='store.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_number', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=250)),
                ('brand', models.CharField(max_length=250, blank=True)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
                ('price', models.DecimalField(default=0.0, max_digits=15, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('product_category', models.CharField(max_length=250, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vendor_name', models.CharField(max_length=200, null=True, blank=True)),
                ('vendor_phone_number', models.CharField(max_length=20, null=True, blank=True)),
                ('vedor_email', models.CharField(max_length=20, null=20, blank=True)),
                ('vendor_address', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(to='store.Vendor'),
        ),
        migrations.AddField(
            model_name='orderedproducts',
            name='product',
            field=models.ForeignKey(to='store.Product'),
        ),
    ]
