# Generated by Django 3.1 on 2020-09-21 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_user_blocked_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hide_recommended_posts',
            field=models.BooleanField(default=False),
        ),
    ]
