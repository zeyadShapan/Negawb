# Generated by Django 3.1 on 2020-09-20 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='blocked_topics',
        ),
    ]