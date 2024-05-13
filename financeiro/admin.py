from django.contrib import admin
from .models import ContaPagar, ContaReceber, Cheque, DespesasCategoria
@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data_vencimento', 'forma_pagamento', 'pago')
    list_filter = ('pago', 'forma_pagamento')
    search_fields = ('descricao', 'forma_pagamento')
    date_hierarchy = 'data_vencimento'

@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data_vencimento', 'forma_recebimento', 'recebido')
    list_filter = ('recebido', 'forma_recebimento')
    search_fields = ('descricao', 'forma_recebimento')
    date_hierarchy = 'data_vencimento'

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nome_titular', 'situacao', 'data_compensacao', 'valor')
    list_filter = ('situacao', 'nome_titular')
    search_fields = ('numero', 'nome_titular')

@admin.register(DespesasCategoria)
class DespesasCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria',)
    search_fields = ('nome_categoria',)



