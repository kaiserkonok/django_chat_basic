from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("chat/", views.index, name="index"),
    path("chat/<str:username>/", views.room, name="room"),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
]