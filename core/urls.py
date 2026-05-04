from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landing/', views.landing, name='landing'),
    path('minha-assinatura/', views.minha_assinatura, name='minha_assinatura'),
    path('403/', views.error_403_view, name='error_403'),

    # Painel do superusuário (dono do sistema)
    path('superuser/', views.superuser_dashboard, name='superuser_dashboard'),
    path('superuser/<uuid:empresa_id>/toggle/', views.superuser_toggle_ativo, name='superuser_toggle_ativo'),
    path('superuser/<uuid:empresa_id>/renovar/', views.superuser_renovar, name='superuser_renovar'),
]
