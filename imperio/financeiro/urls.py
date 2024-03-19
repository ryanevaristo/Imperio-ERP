from django.urls import path
from . import views

app_name = 'financeiro'
urlpatterns = [
    path('contas_pagar/', views.contas_pagar, name='contas_pagar'),
    path('contas_receber/', views.contas_receber, name='contas_receber'),
    path('cheques/', views.cheques, name='cheques'),
]
