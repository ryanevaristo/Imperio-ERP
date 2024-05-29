from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('Usuarios/', views.Usuarios, name='Usuarios'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('excluir_usuario/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('exportar_Usuarios_xlsx/', views.exportar_Usuarios_xlsx, name='exportar_Usuarios_xlsx'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]