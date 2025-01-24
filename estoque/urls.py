from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.home_estoque, name='home_estoque'),
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('editar_produto/<uuid:id>/', views.editar_produto, name='editar_produto'),
    path('deletar_produto/<uuid:id>/', views.deletar_produto, name='deletar_produto'),
    path('detalhes_produto/<uuid:id>/', views.detalhes_produto, name='detalhes_produto'),

]