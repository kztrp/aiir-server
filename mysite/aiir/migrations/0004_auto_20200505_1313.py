# Generated by Django 3.0.5 on 2020-05-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiir', '0003_auto_20200427_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='calculation',
            name='result',
            field=models.BooleanField(default=False),
        ),
    ]
