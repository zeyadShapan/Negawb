# Generated by Django 3.0.8 on 2020-08-14 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0005_auto_20200814_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fixed_navbar',
            field=models.BooleanField(default=True),
        ),
    ]
