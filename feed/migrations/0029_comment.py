# Generated by Django 3.2.19 on 2023-08-26 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0028_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
