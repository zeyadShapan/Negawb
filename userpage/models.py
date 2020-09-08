from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)
    bio = models.CharField(
        max_length=400, default='I love this website!', blank=True, null=True,)
    avatar = models.ImageField(
        upload_to='profile_images', default='profile_images/DefaultUserImage.jpg',)
    phone = models.CharField(max_length=11, null=True, blank=True, unique=True)
    email_code = models.IntegerField(null=True, blank=True)
    phone_code = models.IntegerField(null=True, blank=True)
    # PRIVACY
    show_email = models.BooleanField(default=False)
    who_see_avatar_choices = [
        ('none', 'No One'),
        ('friends', 'Friends only'),
        ('everyone', 'Every One'),
    ]
    who_see_avatar = models.CharField(
        max_length=30,
        choices=who_see_avatar_choices,
        default='friends',
    )
    who_add_group_choices = [
        ('none', 'No One'),
        ('friends', 'Friends Only'),
        ('everyone', 'Every One'),
    ]
    who_add_group = models.CharField(
        max_length=30,
        choices=who_add_group_choices,
        default='friends')
    followers = models.ManyToManyField(
        'User', related_name='user_followers', blank=True)
    is_confirmed = models.BooleanField(default=False)
    allow_friend_request = models.BooleanField(default=True)

    # DISTRACTION FREE!!!!!!!!!!!!!!!
    hide_comments = models.BooleanField(default=False)
    chat_only_mode = models.BooleanField(default=False)
    hide_followed_posts = models.BooleanField(default=False)
    fixed_navbar = models.BooleanField(default=True)
    homepage_hashtags = models.TextField(null=True, blank=True)
    # * notifications
    allow_important_friend_messages = models.BooleanField(default=True)
    allow_important_group_message = models.BooleanField(default=True)
    allow_normal_friend_message = models.BooleanField(default=True)
    allow_normal_group_message = models.BooleanField(default=True)
    allow_comment_message = models.BooleanField(default=True)
    allow_reply_message = models.BooleanField(default=True)
    allow_invites = models.BooleanField(default=True)
    your_invites = models.BooleanField(default=True)

    # IMAGE RESIZING
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.width > 160 or img.height > 160:
                output_size = (160, 160)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
