from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    # Chat Friend
    path('chat_friend/<int:pk>/', views.chat_friend, name='chat_friend'),
    path('send_friend_message/<int:pk>/', views.send_friend_message, name='send_friend_message'),
    path('send_friend_file_message/<int:pk>/', views.send_friend_file_message, name="send_friend_file_message"),
    path('send_friend_voice_message/<int:pk>/', views.send_friend_voice_message, name='send_friend_voice_message'),
    # Chat Group
    path('chat_group/<int:pk>/', views.chat_group, name='chat_group'),
    path('send_group_message/<int:pk>/', views.send_group_message, name='send_group_message'),
    path('send_group_voice_message/<int:pk>/', views.send_group_voice_message, name='send_group_voice_message'),
    path('send_group_file_message/<int:pk>/', views.send_group_file_message, name='send_group_file_message'),
    path('send_group_invite/<int:user_pk>/<int:group_pk>/', views.send_group_invite, name='send_group_invite'),
    path('edit_group/<int:pk>/', views.edit_group, name="edit_group"),
    path('joingroup/',
         views.join_group, name='join_group'),
    path('delete_group/<int:pk>/', views.delete_group, name='delete_group'),
    path('leave_group/<int:pk>/', views.leave_group, name='leave_group'),
    path('denygroup/', views.deny_group, name='deny_group'),
        # Control members
    path('kick_member/<int:group_pk>/<int:member_pk>/', views.kick_member, name='kick_member'),
    path('hire_member/<int:group_pk>/<int:member_pk>/', views.hire_member, name='hire_member'),
    path('lower_member/<int:group_pk>/<int:member_pk>/', views.lower_member, name='lower_member'),

    # Requests
    path('take_down_friend_request/<int:pk>/', views.take_down_friend_request, name='take_down_friend_request'),

    # Area
    path('create_area/<int:pk>/', views.create_area, name='create_area'),
    path('delete_area/<int:pk>/', views.delete_area, name='delete_area'),
    path('load_area/<int:group_pk>/<int:area_pk>/', views.load_area, name='load_area'),
    path('mute_area/<int:pk>/', views.mute_area, name='mute_area'),

    # Notifications
    path('click_notification/<int:pk>/', views.click_notification, name='click_notification'),
    path('delete_all_notifications/', views.delete_all_notifications, name='delete_all_notifications'),
    path('read_all_notifications/', views.read_all_notifications, name='read_all_notifications'),
    
    # users
    path('search_users/', views.search_users, name='search_users'),
]
