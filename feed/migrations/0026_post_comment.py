# Generated by Django 3.2.19 on 2023-08-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0025_rename_comment_store_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
