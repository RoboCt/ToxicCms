from django.urls import path

from userprofile import views

urlpatterns = [
    path('', views.test_view, name='test_view'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('find/', views.find_profile, name='find_profile'),
    path('<int:pk>', views.show_profile, name='show_profile'),
    path('friends/<int:pk>', views.show_friends, name='show_friends'),
]