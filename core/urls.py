from django.contrib import admin
from django.urls import path, include
from core import views
urlpatterns = [
    path('', views.home, name='home'),
    path('403/', views.error_403_view, name='error_403'),
    
]
