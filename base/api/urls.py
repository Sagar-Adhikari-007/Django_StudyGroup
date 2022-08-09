from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoutes, name='getRoutes'),
    path('rooms/', views.getRooms, name='getRooms'),
    path('rooms/<str:pk>/', views.getRoom, name='getRoom'),
]

