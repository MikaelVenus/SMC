# Generated by Django 5.0 on 2023-12-08 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_order_transection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_transection',
            name='receive_phone',
            field=models.CharField(max_length=20),
        ),
    ]
