from django.contrib import admin
from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 
        'cnpj', 
        'mensalidade_ativa', 
        'data_vencimento_mensalidade',
        'mensalidade_valor',
        'status_mensalidade'
    ]
    list_filter = ['mensalidade_ativa', 'data_vencimento_mensalidade']
    search_fields = ['nome', 'cnpj', 'email']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'cnpj', 'endereco', 'telefone', 'email')
        }),
        ('Mensalidade', {
            'fields': (
                'mensalidade_ativa',
                'data_vencimento_mensalidade',
                'mensalidade_valor',
                'mensalidade_dia_vencimento'
            ),
            'description': 'Configurações de mensalidade da empresa'
        }),
    )
    
    def status_mensalidade(self, obj):
        """Exibe o status da mensalidade de forma visual"""
        if obj.pode_acessar_sistema():
            return '✅ Ativa'
        elif obj.mensalidade_vencida():
            return '❌ Vencida'
        else:
            return '⚠️ Inativa'
    
    status_mensalidade.short_description = 'Status'
    
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        """Torna o ID readonly se o objeto já existe"""
        if obj:
            return self.readonly_fields + ['id']
        return self.readonly_fields
