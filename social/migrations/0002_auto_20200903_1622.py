# Generated by Django 3.0.8 on 2020-09-03 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ManyToManyField(default=None, related_name='notification_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='chat_box',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_box', to='social.ChatBox'),
        ),
        migrations.AddField(
            model_name='message',
            name='message_sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grouprequest',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.ChatGroup'),
        ),
        migrations.AddField(
            model_name='grouprequest',
            name='reciever',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grouprequest',
            name='request_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.Area'),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_group', to='social.ChatGroup'),
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='message_sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_message_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatgroup',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatgroup',
            name='group_admins',
            field=models.ManyToManyField(blank=True, related_name='gropu_admins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatgroup',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='group_memebers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatbox',
            name='user_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatbox',
            name='user_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='area',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.ChatGroup'),
        ),
    ]
