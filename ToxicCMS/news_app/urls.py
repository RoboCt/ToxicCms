from django.urls import path

from news_app import views

urlpatterns = [
    path('', views.feed_news, name='feed_news'),
    path('<str:username>', views.feed_news, name='feed_news'),
    path('create/', views.create_feed, name='create_feed'),
    path('edit/<int:pk>', views.edit_feed, name='edit_feed'),
    path('delete/<int:pk>', views.delete_feed, name='delete_feed'),
]