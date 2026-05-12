from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """Endpoint simples para healthcheck do Railway — não acessa o banco."""
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('health/', health_check),
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('', include('core.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('clientes/', include('cliente.urls')),
    path('produto/', include('produto.urls')),
    path('estoque/', include('estoque.urls')),
    path('vendas/', include('vendas.urls')),
    path('api/notifications/', include('notifications.urls')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    




