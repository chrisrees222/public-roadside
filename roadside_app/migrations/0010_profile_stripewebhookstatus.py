# Generated by Django 4.2.6 on 2024-01-01 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadside_app', '0009_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripeWebHookStatus',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
