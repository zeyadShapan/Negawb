from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'userpage'

urlpatterns = [
    path('edit_user/', views.edit_user, name='edit_user'),
    path('posts/', views.posts, name='posts'),
    path('friends/', views.friends, name='friends'),
    path('requests/', views.requests, name='requests'),
    path('invites/', views.invites, name='invites'),

    path('denyrequest/',
         views.denyrequest, name='denyrequest'),
    path('acceptrequest/',
         views.acceptrequest, name='acceptrequest'),
    path('unfriend/<int:pk>/', views.unfriend, name='unfriend'),
    path('get_user_by_id/', views.get_user_by_id, name='get_user_by_id'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
