# Generated by Django 5.1.5 on 2025-02-21 06:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_coupons_alter_cartorder_order_date_cartorder_coupons'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.vendor'),
        ),
    ]
