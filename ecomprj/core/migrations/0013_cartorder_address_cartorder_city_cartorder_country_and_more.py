# Generated by Django 5.1.5 on 2025-02-19 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_cartorderitems_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='country',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='mobile',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='saved',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='stripe_payment_intent',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='tracking_website_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
