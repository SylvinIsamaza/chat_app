# Generated by Django 3.2.19 on 2023-08-26 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0023_comment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Comment_store',
        ),
    ]
