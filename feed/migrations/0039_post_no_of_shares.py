# Generated by Django 3.2.19 on 2023-08-27 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0038_rename_share_post_shared_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='no_of_shares',
            field=models.IntegerField(default=0),
        ),
    ]
