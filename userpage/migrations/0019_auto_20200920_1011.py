# Generated by Django 3.1 on 2020-09-20 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_auto_20200920_1004'),
        ('userpage', '0018_remove_user_company_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='homepage_hashtags',
        ),
        migrations.AddField(
            model_name='user',
            name='blocked_topics',
            field=models.ManyToManyField(to='categories.Category'),
        ),
    ]