from django.urls import path
from . import views

app_name = 'financeiro'
urlpatterns = [
    #despesas
    path('despesas/', views.despesas, name='despesas'),
    path('cadastrar_despesas/', views.cadastrar_despesas, name='cadastrar_despesas'),
    path('editar_despesas/<int:id>/', views.editar_despesas, name='editar_despesas'),
    path('excluir_despesas/<int:id>/', views.excluir_despesas, name='excluir_despesas'),
    path('total_despesas_mes_atual/', views.total_despesas_m_atual, name='total_despesas_mes_atual'),
    path('total_despesas', views.total_despesas, name='total_despesas'),
    path('exportar_despesas_xlsx', views.exportar_despesas_xlsx, name='exportar_despesas_xlsx'),
    path('exportar_despesas_pdf', views.exportar_despesas_pdf, name='exportar_despesas_pdf'),
    #categorias
    path('cadastrar_categoria/', views.cadastrar_categorias, name='cadastrar_categoria'),
    #contas a receber
    path('entrada/', views.entrada, name='entradas'),
    path('cadastrar_entrada/', views.cadastrar_entrada, name='cadastrar_entrada'),
    path('editar_entrada/<int:id>/', views.editar_entrada, name='editar_entrada'),
    path('excluir_entrada/<int:id>/', views.excluir_entrada, name='excluir_entrada'),
    path('total_entradas', views.total_entradas, name='total_entradas'),
    path('exportar_entradas_xlsx', views.exportar_entrada_xlsx, name='exportar_entradas_xlsx'),
    #cheques
    path('cheques/', views.cheques, name='cheques'),
    path('cadastrar_cheque/', views.cadastrar_cheque, name='cadastrar_cheque'),
    path('editar_cheque/<int:id>/', views.editar_cheque, name='editar_cheque'),
    path('excluir_cheque/<int:id>/', views.excluir_cheque, name='excluir_cheque'),
    path('total_cheques', views.total_cheques, name='total_cheques'),
    path('exportar_cheques_xlsx', views.exportar_cheque_xlsx, name='exportar_cheques_xlsx'),
    #fornecedores
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('cadastrar_fornecedor/', views.cadastrar_fornecedor, name='cadastrar_fornecedor'),
    path('editar_fornecedor/<int:id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('excluir_fornecedor/<int:id>/', views.excluir_fornecedor, name='excluir_fornecedor'),
    #caixa
    path('caixa/', views.caixa, name='caixa'),
    
    
]
