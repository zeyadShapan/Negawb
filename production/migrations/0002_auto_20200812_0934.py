# Generated by Django 3.0.8 on 2020-08-12 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='tags',
            new_name='tag',
        ),
    ]