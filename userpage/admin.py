from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model as user_model
User = user_model()


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('friends', 'bio', 'avatar', 'show_email', 'who_see_avatar', 'who_add_group', 'followers', 'is_confirmed', 'allow_friend_request', 'hide_comments', 'chat_only_mode', 'hide_followed_posts', 'fixed_navbar',
                           'homepage_hashtags', 'allow_important_friend_messages', 'allow_important_group_message', 'allow_normal_friend_message', 'allow_normal_group_message', 'allow_comment_message', 'allow_reply_message', 'allow_invites', 'your_invites',)}),
    )


admin.site.register(User, MyUserAdmin)
