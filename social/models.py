from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatBox(models.Model):
    user_1 = models.ForeignKey(
        User, related_name='user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(
        User, related_name='user_2', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_1} and {self.user_2}'


class Message(models.Model):
    chat_box = models.ForeignKey(
        ChatBox, related_name='chat_box', null=True, on_delete=models.CASCADE)
    message_sender = models.ForeignKey(
        User, related_name='message_sender', null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(
        upload_to='social_group_message_images', blank=True, null=True)
    image = models.ImageField(
        upload_to='social/friend_message_images', blank=True, null=True)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.message_sender} to ({self.chat_box}) ⚠️{self.is_important}⚠️'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 140 or img.height > 140:
                output_size = (140, 140)
                img.thumbnail(output_size)
                img.save(self.image.path)


class ChatGroup(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='group_images',
                              default='profile_images/DefaultUserImage.jpg')
    is_public = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    # USERS
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group_admins = models.ManyToManyField(
        User, related_name='gropu_admins', blank=True)
    members = models.ManyToManyField(
        User, related_name='group_memebers', blank=True)

    def __str__(self):
        return f'[AUTHOR] {self.author} [TITLE] {self.title} [MEMBERS] {self.members.count()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 140 or img.height > 140:
                output_size = (140, 140)
                img.thumbnail(output_size)
                img.save(self.image.path)


class GroupRequest(models.Model):
    request_sender = models.ForeignKey(
        User, related_name='request_sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[GROUP] {self.group.title} | {self.request_sender} To {self.reciever}'


class Area(models.Model):
    name = models.CharField(max_length=20)
    mute = models.BooleanField(default=False)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    group = models.ForeignKey(
        ChatGroup, related_name='chat_group', null=True, on_delete=models.CASCADE)
    message_sender = models.ForeignKey(
        User, related_name='group_message_sender', null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)
    # //////// Files
    file = models.FileField(
        upload_to='social/group_files', null=True, blank=True)
    video = models.FileField(upload_to='social/group_videos', null=True, blank=True)
    image = models.ImageField(
        upload_to='social/group_images', null=True, blank=True)
    audio = models.ImageField(
        upload_to='social/group_audio', null=True, blank=True)
    # Files ////////
    is_important = models.BooleanField(default=False)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.message_sender}, {self.message} chat_box: {self.group}'

    # IMAGE RESIZING
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 450 or img.height > 349:
                output_size = (450, 349)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Notification(models.Model):
    notification_type_choices = [
        # Messages
        # * important
        ('important_friend_message', 'important_friend_message'),
        ('important_group_message', 'important_group_message'),
        # * noraml
        ('normal_friend_message', 'normal_friend_message'),
        ('normal_group_message', 'normal_group_message'),
        # Society
        ('comment_message', 'comment_message'),
        ('reply_message', 'reply_message'),
        # Invites
        # * others
        ('invites', 'invites'),
        # * you
        ('your_invites', 'your_invites'),
    ]
    notification_type = models.CharField(
        max_length=50, choices=notification_type_choices)
    receiver = models.ManyToManyField(
        User, related_name="notification_receiver", default=None)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_sender')
    content = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
