# Generated by Django 3.0.8 on 2020-09-08 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0006_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='homepage_posts',
            field=models.TextField(blank=True, null=True),
        ),
    ]
