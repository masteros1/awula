# Generated by Django 5.0.3 on 2024-05-23 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_user_customer_user_alter_order_transaction_id_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='order',
            name='unique_incomplete_order_per_customer',
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.UniqueConstraint(condition=models.Q(('complete', False)), fields=('customer',), name='unique_incomplete_order_per_customer'),
        ),
    ]
