# Generated by Django 3.2.19 on 2023-08-26 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0026_post_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post_comment',
        ),
    ]