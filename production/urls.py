from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.create_todo, name='create_todo'), 
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/<int:pk>/', views.ViewFeedback.as_view(), name='ViewFeedback'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('update_todo/<int:pk>/', views.update_todo, name='update_todo')
]
