from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('', views.home_vendas, name='home_vendas'),
    path('cadastrar/', views.cadastrar_venda, name='cadastrar_venda'),
    path('<uuid:pk>/', views.detalhe_venda, name='detalhe_venda'),
    path('<uuid:pk>/pagamento/', views.registrar_pagamento, name='registrar_pagamento'),
    path('<uuid:pk>/cancelar/', views.cancelar_venda, name='cancelar_venda'),
]
