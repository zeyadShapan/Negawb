# Generated by Django 3.1 on 2020-09-18 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmessage',
            name='video',
        ),
    ]
