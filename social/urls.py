from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('create_ChatBox/<int:friend_id>/',
         views.create_ChatBox, name='create_ChatBox'),
    path('chat_friend/<int:friend_id>/', views.chat_friend, name='chat_friend'),
    path('createchatgroup/', views.create_chat_group, name='create_chat_group'),
    path('mygroups/', views.my_groups, name='my_groups'),
    path('mygroups/<int:chatgroup_pk>/', views.view_group, name='view_group'),
    path('groupinvite/<int:pk>/', views.groupinvite, name='groupinvite'),
    path('createinvite/<int:user_pk>/<int:group_pk>/',
         views.create_invite, name='create_invite'),
    path('joingroup/<int:pk>/',
         views.join_group, name='join_group'),
    path('denygroup/<int:pk>/', views.deny_group, name='deny_group'),
]