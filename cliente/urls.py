from django.urls import path
from .views import listar_clientes, cadastrar_clientes, editar_clientes, deletar_clientes

app_name = 'cliente'
urlpatterns = [
    path('', listar_clientes, name='listar_clientes'),
    path('cadastrar/', cadastrar_clientes, name='cadastrar_clientes'),
    path('editar/<int:id>/', editar_clientes, name='editar_clientes'),
    path('deletar/<int:id>/', deletar_clientes, name='deletar_clientes'),
]