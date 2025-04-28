from django.contrib import admin
from .models import EstoqueCategoria, Produtos

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto','qtd')

@admin.register(EstoqueCategoria)
class EstoqueCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria',)
    search_fields = ('nome_categoria',)



# Register your models here.
