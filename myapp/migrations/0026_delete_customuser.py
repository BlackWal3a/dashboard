# Generated by Django 4.2.7 on 2024-03-14 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_customuser_delete_extendeduser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]