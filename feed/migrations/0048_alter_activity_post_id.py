# Generated by Django 3.2.19 on 2023-09-12 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0047_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='post_id',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]