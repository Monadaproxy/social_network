from django.urls import path
from . import views
from .views import ArticlesAPIView

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('api', ArticlesAPIView.as_view(), name='api_news_home'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='news-delete'),
] 