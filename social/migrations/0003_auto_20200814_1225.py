# Generated by Django 3.0.8 on 2020-08-14 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20200811_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='image',
            field=models.ImageField(default='profile_images/DefaultUserImage.WebP', upload_to='group_images'),
        ),
    ]