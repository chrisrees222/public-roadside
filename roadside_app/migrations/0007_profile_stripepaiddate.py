# Generated by Django 4.2.7 on 2023-12-31 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadside_app', '0006_remove_profile_stripe_customer_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripePaidDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]