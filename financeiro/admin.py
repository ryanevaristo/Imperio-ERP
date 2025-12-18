from django.contrib import admin
from .models import ContaPagar, ContaReceber, Cheque, DespesasCategoria
@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor','forma_pagamento', 'pago')
    list_filter = ('pago', 'forma_pagamento')
    search_fields = ('descricao', 'forma_pagamento')

@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'forma_recebimento', 'recebido', 'empresa')
    list_filter = ('recebido', 'forma_recebimento', 'empresa')
    search_fields = ('descricao', 'forma_recebimento')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nome_titular', 'situacao', 'data_compensacao', 'valor', 'empresa')
    list_filter = ('situacao', 'nome_titular', 'empresa')
    search_fields = ('numero', 'nome_titular')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

@admin.register(DespesasCategoria)
class DespesasCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria', 'empresa')
    list_filter = ('empresa',)
    search_fields = ('nome_categoria',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)



