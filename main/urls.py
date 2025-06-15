from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_index, name='home'),
    path('about/', views.about_about, name='about')
]