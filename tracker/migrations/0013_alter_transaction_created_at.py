# Generated by Django 5.1.4 on 2024-12-19 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0012_alter_transaction_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(verbose_name='Дата'),
        ),
    ]
