from django.contrib import admin
from .models import EstoqueCategoria, Produtos, Movimentacao, Notificacao

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto','qtd')

@admin.register(EstoqueCategoria)
class EstoqueCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria',)
    search_fields = ('nome_categoria',)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'qtd', 'tipo', 'created_at')
    list_filter = ('tipo', 'created_at')
    ordering = ('created_at',)
#         categoria = EstoqueCategoria.objects.get(id=request.POST.get('categoria'))


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'mensagem',  'data_criacao','visualizado' )
    list_filter = ('visualizado', 'data_criacao')
    ordering = ('data_criacao',)