# Generated by Django 3.2.19 on 2023-08-26 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0024_rename_comment_comment_store'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment_store',
            new_name='Comment',
        ),
    ]
