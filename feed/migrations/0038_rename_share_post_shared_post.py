# Generated by Django 3.2.19 on 2023-08-27 07:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0037_saved_post_share_post'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Share_Post',
            new_name='Shared_Post',
        ),
    ]