from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('', include('core.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('clientes/', include('cliente.urls')),
    path('produto/', include('produto.urls')),
    path('estoque/', include('estoque.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    




