from django.urls import path
from . import views

app_name = 'produto'
urlpatterns = [
    path('', views.home_produto, name='home_produto'),
    path('cadastrar_empreendimento/', views.cadastrar_empreendimento, name='cadastrar_empreendimento'),
    path('detalhes_empreendimento/<uuid:id>/', views.detalhes_empreendimento, name='detalhes_empreendimento'),
    path('cadastrar_quadra/<uuid:id>/', views.cadastrar_quadra, name='cadastrar_quadra'),
    path('quadras/<uuid:id>/', views.quadras, name='quadras'),
    path('lotes/<uuid:id>/', views.lotes, name='lotes'),
]
