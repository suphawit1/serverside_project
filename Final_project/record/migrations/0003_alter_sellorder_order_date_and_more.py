# Generated by Django 5.1.1 on 2024-10-14 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_alter_purchaseorders_date_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellorder',
            name='order_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateField(auto_now=True),
        ),
    ]
