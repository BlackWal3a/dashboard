# Generated by Django 4.2.7 on 2024-04-14 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_account_geography_filter_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='dark_mode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]