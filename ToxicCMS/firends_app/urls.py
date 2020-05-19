from django.urls import path

from firends_app import views

urlpatterns = [
    path('', views.friends_list, name='friends_list'),
    path('request/', views.add_friend_request, name='request_friend'),
    path('accept/', views.confirm_friend_request, name='accept_friend'),
    path('remove/<int:pk>', views.remove_friend, name='remove_friend'),
]