# Generated by Django 3.2.19 on 2023-08-21 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.IntegerField(default=0),
        ),
    ]
