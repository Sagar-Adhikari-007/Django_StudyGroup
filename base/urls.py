from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('createRoom/', views.createRoom, name='createRoom'),
    path('updateRoom/<str:pk>/', views.updateRoom, name='updateRoom'),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name='deleteRoom'),
    path('deleteComment/<str:pk>/', views.deleteComment, name='deleteComment'),
    path('profile/<str:pk>/', views.userProfile, name='userProfile'),
    path('update-user/', views.updateUser, name='updateUser'),
    path('topics/', views.topicsPage, name='topicsPage'),
    path('activity/', views.activityPage, name='activityPage'),
]