# Generated by Django 3.0.8 on 2020-09-03 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('stars', models.CharField(choices=[('✭', '✭ Very Bad'), ('✭✭', '✭✭ Bad'), ('✭✭✭', '✭✭✭ Ok'), ('✭✭✭✭', '✭✭✭✭ Good'), ('✭✭✭✭✭', '✭✭✭✭✭ Excellent')], max_length=15)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('note', models.TextField(blank=True, null=True)),
                ('is_important', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
