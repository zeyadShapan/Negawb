# Generated by Django 3.0.8 on 2020-08-19 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_auto_20200818_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='image',
            field=models.ImageField(default='profile_images/DefaultUserImage.WebP', upload_to='group_images'),
        ),
    ]
