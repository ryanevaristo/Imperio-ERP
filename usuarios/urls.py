from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'
urlpatterns = [
    # Usuários internos (admin only)
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('Usuarios/', views.Usuarios, name='Usuarios'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('excluir_usuario/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('exportar_Usuarios_xlsx/', views.exportar_Usuarios_xlsx, name='exportar_Usuarios_xlsx'),

    # Autenticação
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Cadastro self-service
    path('cadastro/', views.cadastro, name='cadastro'),

    # Recuperação de senha (Django built-in com templates customizados)
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.txt',
        subject_template_name='password_reset_subject.txt',
        success_url='/auth/recuperar-senha/enviado/',
    ), name='password_reset'),

    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html',
    ), name='password_reset_done'),

    path('recuperar-senha/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/auth/recuperar-senha/concluido/',
    ), name='password_reset_confirm'),

    path('recuperar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html',
    ), name='password_reset_complete'),
]