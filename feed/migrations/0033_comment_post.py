# Generated by Django 3.2.19 on 2023-08-27 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0032_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='feed.post'),
        ),
    ]
