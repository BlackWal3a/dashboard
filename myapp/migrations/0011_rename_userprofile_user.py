# Generated by Django 4.2.7 on 2024-03-06 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_userprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='User',
        ),
    ]