# Generated by Django 3.0.8 on 2020-09-03 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0002_auto_20200903_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]