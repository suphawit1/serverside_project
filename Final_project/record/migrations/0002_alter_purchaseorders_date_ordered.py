# Generated by Django 5.1.1 on 2024-10-12 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorders',
            name='date_ordered',
            field=models.DateField(auto_now=True),
        ),
    ]
