from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('cadastrar_vendedor/', views.cadastrar_vendedor, name='cadastrar_vendedor'),
    path('listar_vendedor/', views.listar_vendedor, name='listar_vendedor'),
    path('editar_vendedor/<int:id>/', views.editar_vendedor, name='editar_vendedor'),
    path('excluir_vendedor/<int:id>/', views.excluir_vendedor, name='excluir_vendedor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]