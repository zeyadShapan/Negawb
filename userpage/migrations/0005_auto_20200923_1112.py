# Generated by Django 3.1 on 2020-09-23 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0004_auto_20200921_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image_rate',
            field=models.IntegerField(default=33),
        ),
        migrations.AddField(
            model_name='user',
            name='text_rate',
            field=models.IntegerField(default=33),
        ),
        migrations.AddField(
            model_name='user',
            name='video_rate',
            field=models.IntegerField(default=33),
        ),
    ]
