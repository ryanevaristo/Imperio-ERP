from django.contrib import admin
from .models import Cliente

admin.site.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cnpj_cpf', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'data_cadastro')
    search_fields = ('nome_completo', 'cnpj_cpf', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'data_cadastro')
    list_filter = ('nome_completo', 'cnpj_cpf', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'data_cadastro')
    list_per_page = 10


# Register your models here.
