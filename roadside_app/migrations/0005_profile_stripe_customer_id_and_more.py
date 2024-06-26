# Generated by Django 4.2.7 on 2023-12-26 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadside_app', '0004_remove_profile_customer_remove_profile_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
