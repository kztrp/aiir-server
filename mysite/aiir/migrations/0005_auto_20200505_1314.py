# Generated by Django 3.0.5 on 2020-05-05 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiir', '0004_auto_20200505_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='progress',
            field=models.FloatField(default=0),
        ),
    ]