# Generated by Django 4.2.7 on 2024-03-12 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_deliveryorder_delete_deliveryorders'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(max_length=100, null=True, unique=True)),
                ('Quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('StartOperation', models.CharField(max_length=100)),
                ('StopOperation', models.CharField(max_length=100)),
                ('FlightsDate', models.CharField(max_length=100)),
                ('AircraftCode', models.CharField(max_length=100, null=True)),
                ('AircraftName', models.CharField(max_length=100, null=True)),
                ('ProviderCode', models.CharField(max_length=100, null=True)),
                ('Provider', models.CharField(max_length=100, null=True)),
                ('UnitCode', models.CharField(max_length=100)),
                ('Unit', models.CharField(max_length=100)),
                ('StopOverCode', models.CharField(max_length=100, null=True)),
                ('StopOver', models.CharField(max_length=100, null=True)),
                ('TownCode', models.CharField(max_length=100, null=True)),
                ('Town', models.CharField(max_length=100, null=True)),
                ('CountryCode', models.CharField(max_length=100, null=True)),
                ('Country', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='DeliveryOrder',
        ),
    ]
