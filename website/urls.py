from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_, name="login"),
    path('logout/', views.logout_, name="logout"),
    path('items/', views.items, name="items"),
    path('additem/', views.additem, name="additem"),
    path('notification/<str:days>', views.notification, name="notification"),
    path('about/', views.about, name="about"),
]
