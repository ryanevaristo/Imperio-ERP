from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','nome_completo', 'cpf_cnpj', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'data_cadastro')
    search_fields = ('nome_completo', 'cpf_cnpj', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'data_cadastro')
    list_filter = ('nome_completo', 'cpf_cnpj', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'data_cadastro')
    list_per_page = 10


# Register your models here.
