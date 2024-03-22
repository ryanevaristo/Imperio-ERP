from django.urls import path
from . import views

app_name = 'financeiro'
urlpatterns = [
    path('', views.financeiro, name='financeiro'),
    #contas a pagar
    path('contas_pagar/', views.contas_pagar, name='contas_pagar'),
    path('cadastrar_contas_pagar/', views.cadastrar_contas_pagar, name='cadastrar_contas_pagar'),
    path('editar_contas_pagar/<int:id>/', views.editar_contas_pagar, name='editar_contas_pagar'),
    path('excluir_contas_pagar/<int:id>/', views.excluir_contas_pagar, name='excluir_contas_pagar'),
    #contas a receber
    path('contas_receber/', views.contas_receber, name='contas_receber'),
    path('cadastrar_contas_receber/', views.cadastrar_contas_receber, name='cadastrar_contas_receber'),
    path('editar_contas_receber/<int:id>/', views.editar_contas_receber, name='editar_contas_receber'),
    path('excluir_contas_receber/<int:id>/', views.excluir_contas_receber, name='excluir_contas_receber'),
    #cheques
    path('cheques/', views.cheques, name='cheques'),
    path('cadastrar_cheque/', views.cadastrar_cheque, name='cadastrar_cheque'),
    path('editar_cheque/<int:id>/', views.editar_cheque, name='editar_cheque'),
    path('excluir_cheque/<int:id>/', views.excluir_cheque, name='excluir_cheque'),
    
]
