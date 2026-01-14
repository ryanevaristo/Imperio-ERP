from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.home_estoque, name='home_estoque'),
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('editar_produto/<uuid:id>/', views.editar_produto, name='editar_produto'),
    path('deletar_produto/<uuid:id>/', views.deletar_produto, name='deletar_produto'),
    path('detalhes_produto/<uuid:id>/', views.detalhes_produto, name='detalhes_produto'),
    # MOVIENTAÇÕES
    path("registrar-movimentacao/", views.registrar_movimentacao, name="registrar_movimentacao"),

    path('notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),
    path('marcar_vizualizado/<int:id>/', views.marca_vizualizado, name='marcar_visualizado'),
    path('historico_todas_movimentacoes/', views.historico_todas_movimentacoes, name='historico_todas_movimentacoes'),

    #JSON
    path('get_quadras/<uuid:empreendimento_id>/', views.get_quadras, name='get_quadras'),
    path('get_lotes/<uuid:quadra_id>/', views.get_lotes, name='get_lotes'),
    path("buscar-produtos/", views.buscar_produtos, name="buscar_produtos"),



    # IMPORTAÇÂO E EXPORTAÇÃO
    path('importar_estoque_excel/', views.importar_estoque_excel, name='importar_estoque_excel'),
    path('exportar_estoque_xls/', views.exportar_estoque_xls, name='exportar_estoque_xls'),
    path('exportar_estoque_pdf/', views.exportar_estoque_pdf, name='exportar_estoque_pdf'),
    path('exportar_movimentacao_xlsx/', views.exportar_movimentacao_xlsx, name='exportar_movimentacao_xlsx'),
    path('exportar_movimentacao_pdf/', views.exportar_movimentacao_pdf, name='exportar_movimentacao_pdf'),


]