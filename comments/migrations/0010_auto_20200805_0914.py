# Generated by Django 3.0.8 on 2020-08-05 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_auto_20200805_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]