# Generated by Django 5.0.3 on 2024-04-05 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.IntegerField(),
        ),
    ]
