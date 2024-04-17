from django.urls import path
from . import views

app_name = 'financeiro'
urlpatterns = [
    #despesas
    path('despesas/', views.despesas, name='despesas'),
    path('cadastrar_despesas/', views.cadastrar_despesas, name='cadastrar_despesas'),
    path('editar_despesas/<int:id>/', views.editar_despesas, name='editar_despesas'),
    path('excluir_despesas/<int:id>/', views.excluir_despesas, name='excluir_despesas'),
    path('total_despesas/', views.total_despesas, name='total_despesas'),
    #categorias
    path('cadastrar_categoria/', views.cadastrar_categorias, name='cadastrar_categoria'),
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
    #fornecedores
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('cadastrar_fornecedor/', views.cadastrar_fornecedor, name='cadastrar_fornecedor'),
    path('editar_fornecedor/<int:id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('excluir_fornecedor/<int:id>/', views.excluir_fornecedor, name='excluir_fornecedor'),
    
    
]
