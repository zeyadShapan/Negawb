from django.forms import ModelForm
from django.contrib.auth import get_user_model as user_model
User = user_model()


class UserForm(ModelForm):
    """Update User after creating it from user page"""

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'avatar')


class UserPrivacyForm(ModelForm):
    class Meta:
        model = User
        fields = ('show_email', 'who_see_avatar',
                  'who_add_group', 'allow_friend_request')
        labels = {'who_add_group': 'Who can add me to groups',
                  'who_see_avatar': 'Who can see profile image'}


class DistractionFreeForm(ModelForm):
    class Meta:
        model = User
        fields = ('hide_comments', 'fixed_navbar','hide_posts_in_homepage', 'homepage_posts', 'allow_important_friend_messages', 'allow_important_group_message', 'allow_normal_friend_message', 'allow_normal_group_message',
                'allow_comment_message', 'allow_reply_message', 'allow_invites', 'your_invites', 'blocked_categories', 'chat_only_mode',)
        labels = {
            'allow_important_friend_messages': 'Friend\'s important message',
            'allow_important_group_message': 'Group important message',
            'allow_important_group_message': 'Group important message',
            'allow_normal_friend_message': 'Friend\'s normal message',
            'allow_normal_group_message': 'Group normal message',
            'allow_comment_message': 'Post Comments',
            'allow_reply_message': 'Comment replies',
            'allow_invites': 'friend and group <b>Invites</b>',
            'your_invites':'Your own invites',
            'homepage_posts': 'Posts to show in homepage <small class="form-text text-muted">choose none if you don\'t want to show posts in homepage</small>',
            'hide_posts_in_homepage':'Hide Friends posts in homepage'
        }
