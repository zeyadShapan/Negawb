# Generated by Django 3.0.8 on 2020-08-27 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_auto_20200827_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='date_completed',
        ),
        migrations.RemoveField(
            model_name='note',
            name='is_completed',
        ),
    ]