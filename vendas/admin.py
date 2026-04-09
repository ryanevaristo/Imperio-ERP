from django.contrib import admin
from .models import Vendas, Pagamento


class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    readonly_fields = ('data_pagamento',)


@admin.register(Vendas)
class VendasAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'id_lote', 'valor_venda', 'status_venda', 'quitado', 'data_venda', 'empresa')
    list_filter = ('status_venda', 'quitado', 'empresa')
    search_fields = ('id_cliente__nome_completo', 'id_lote__numero')
    inlines = [PagamentoInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id_venda', 'forma_pagamento', 'valor', 'data_pagamento', 'empresa')
    list_filter = ('forma_pagamento', 'empresa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)
