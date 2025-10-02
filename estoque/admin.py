from django.contrib import admin
from django import forms
from .models import EstoqueCategoria, Produtos, Movimentacao, Notificacao

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = '__all__'

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto','qtd')

@admin.register(EstoqueCategoria)
class EstoqueCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria',)
    search_fields = ('nome_categoria',)




@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    form = MovimentacaoForm
    list_display = ('produto', 'qtd', 'tipo', 'created_at')
    list_filter = ('tipo', 'created_at')
    ordering = ('created_at',)
    fields = ('produto', 'qtd', 'tipo', 'motivo', 'empreendimento', 'quadra', 'lote')

    def save_model(self, request, obj, form, change):
        # Salva o objeto primeiro
        super().save_model(request, obj, form, change)
        
        # Atualiza a quantidade do produto no estoque
        produto = obj.produto
        if obj.tipo == 'Entrada':
            produto.qtd += obj.qtd
        elif obj.tipo == 'Saida':
            produto.qtd -= obj.qtd
        elif obj.tipo == 'Devolucao':
            produto.qtd += obj.qtd
        
        # Verifica se a quantidade não fica negativa
        if produto.qtd < 0:
            # Reverte a mudança se negativa
            if obj.tipo == 'Entrada':
                produto.qtd -= obj.qtd
            elif obj.tipo == 'Saida':
                produto.qtd += obj.qtd
            elif obj.tipo == 'Devolucao':
                produto.qtd -= obj.qtd
            raise ValueError("Quantidade não pode ser negativa!")
        
        produto.save()
        
        # Verifica se precisa criar notificação
        if produto.qtd <= produto.qtd_min:
            from .models import Notificacao
            Notificacao.objects.create(
                produto=produto,
                mensagem=f'O produto {produto.produto} está abaixo ou no mínimo do estoque!'
            )

    class Media:
        js = ('estoque/js/dependent_selects.js',)


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'mensagem',  'data_criacao','visualizado' )
    list_filter = ('visualizado', 'data_criacao')
    ordering = ('data_criacao',)