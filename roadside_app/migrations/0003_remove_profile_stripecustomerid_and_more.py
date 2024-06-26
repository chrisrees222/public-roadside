# Generated by Django 4.2.6 on 2023-12-26 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0012_2_8'),
        ('roadside_app', '0002_alter_profile_stripecustomerid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='stripeCustomerId',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='stripeSubscriptionId',
        ),
        migrations.AddField(
            model_name='profile',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.customer'),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.subscription'),
        ),
    ]
