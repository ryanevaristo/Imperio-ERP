from django.contrib import admin
from django import forms
from .models import EstoqueCategoria, Produtos, Movimentacao, Notificacao, MovimentacaoItem

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = '__all__'


class MovimentacaoItemInline(admin.TabularInline):
    model = MovimentacaoItem
    extra = 0
    fields = ('produto', 'qtd')
    readonly_fields = ('produto', 'qtd')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto','qtd', 'empresa')
    list_filter = ('empresa',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)


@admin.register(EstoqueCategoria)
class EstoqueCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria',)
    search_fields = ('nome_categoria',)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    form = MovimentacaoForm
    list_display = ('tipo', 'motivo', 'created_at', 'empresa', 'get_total_itens')
    list_filter = ('tipo', 'created_at', 'empresa')
    ordering = ('-created_at',)
    fields = ('tipo', 'motivo', 'empreendimento', 'quadra', 'lote', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [MovimentacaoItemInline]
    
    def get_total_itens(self, obj):
        return obj.itens.count()
    get_total_itens.short_description = 'Total de Itens'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

    class Media:
        js = ('estoque/js/dependent_selects.js',)


@admin.register(MovimentacaoItem)
class MovimentacaoItemAdmin(admin.ModelAdmin):
    list_display = ('get_movimentacao_tipo', 'produto', 'qtd', 'get_movimentacao_data', 'empresa')
    list_filter = ('movimentacao__tipo', 'movimentacao__created_at', 'empresa', 'produto')
    search_fields = ('produto__produto', 'movimentacao__motivo')
    ordering = ('-movimentacao__created_at',)
    readonly_fields = ('movimentacao', 'produto', 'qtd', 'empresa')
    
    def get_movimentacao_tipo(self, obj):
        return obj.movimentacao.get_tipo_display()
    get_movimentacao_tipo.short_description = 'Tipo de Movimentação'
    get_movimentacao_tipo.admin_order_field = 'movimentacao__tipo'
    
    def get_movimentacao_data(self, obj):
        return obj.movimentacao.created_at.strftime('%d/%m/%Y %H:%M')
    get_movimentacao_data.short_description = 'Data'
    get_movimentacao_data.admin_order_field = 'movimentacao__created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'mensagem',  'data_criacao','visualizado', 'empresa' )
    list_filter = ('visualizado', 'data_criacao', 'empresa')
    ordering = ('data_criacao',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)
