# Generated by Django 5.1.4 on 2024-12-08 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_rename_data_tracker_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='description',
            field=models.CharField(default=1, max_length=50, verbose_name='Опис'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tracker',
            name='amount',
            field=models.CharField(max_length=10, verbose_name='Количество'),
        ),
    ]
