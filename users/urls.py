from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('upload-avatar/', views.upload_avatar, name='upload_avatar'),
    path('profile/<str:username>/edit', views.profile_edit, name='profile_edit'),
]

