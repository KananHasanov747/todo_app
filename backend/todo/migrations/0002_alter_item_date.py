# Generated by Django 5.0.6 on 2024-05-15 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date',
            field=models.DateTimeField(verbose_name='Date'),
        ),
    ]
