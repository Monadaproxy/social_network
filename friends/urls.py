from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.friend_list, name='friend_list'),
    path('requests/', views.friendship_requests, name='friendship_requests'),
    path('request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('request/<int:request_id>/handle/', views.handle_friend_request, name='handle_friend_request'),
]