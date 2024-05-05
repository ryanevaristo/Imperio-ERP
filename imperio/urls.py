
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('', include('core.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('clientes/', include('cliente.urls')),
]
