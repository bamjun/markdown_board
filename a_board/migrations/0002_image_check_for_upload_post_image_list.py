# Generated by Django 5.0.7 on 2024-07-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='check_for_upload',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='image_list',
            field=models.JSONField(default=list),
        ),
    ]