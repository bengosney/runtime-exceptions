# Generated by Django 3.0.2 on 2020-01-16 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strava', '0009_auto_20200116_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runner',
            name='access_expires',
            field=models.CharField(max_length=512),
        ),
    ]