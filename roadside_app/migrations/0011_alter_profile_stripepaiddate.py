# Generated by Django 4.2.6 on 2024-01-01 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadside_app', '0010_profile_stripewebhookstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='stripePaidDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
