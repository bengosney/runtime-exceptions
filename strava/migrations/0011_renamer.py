# Generated by Django 3.0.2 on 2020-01-26 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strava', '0010_auto_20200116_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Renamer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('name', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
            ],
        ),
    ]