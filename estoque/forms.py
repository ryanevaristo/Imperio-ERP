# forms.py (no app estoque)
from django import forms
from django.core.exceptions import ValidationError
from .models import Produtos, EstoqueCategoria, Movimentacao
from produto.models import Empreendimento, Quadra, Lote  # Assumindo que estão em outro app

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = EstoqueCategoria
        fields = ['nome_categoria']  # Ajuste o campo se for 'descricao' no seu model
        widgets = {
            'nome_categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nome_categoria(self):
        nome = self.cleaned_data['nome_categoria']
        if EstoqueCategoria.objects.filter(nome_categoria=nome).exists():
            raise ValidationError('Categoria já cadastrada.')
        return nome

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = ['produto', 'qtd', 'qtd_min', 'custo', 'venda', 'categoria']
        widgets = {
            'produto': forms.TextInput(attrs={'class': 'form-control'}),
            'qtd': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'qtd_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'custo': forms.DecimalField(attrs={'class': 'form-control'}),
            'venda': forms.DecimalField(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        custo = cleaned_data.get('custo')
        venda = cleaned_data.get('venda')
        if custo and venda and custo > 0:
            margem = ((float(venda) - float(custo)) / float(custo)) * 100
            self.instance.Margem = round(margem, 2)  # Calcula margem automaticamente
        if not cleaned_data.get('categoria'):
            raise ValidationError('Selecione uma categoria.')
        return cleaned_data

class EditarProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = ['produto', 'qtd', 'preco', 'descricao', 'categoria']  # Ajuste campos conforme seu model
        widgets = {
            'produto': forms.TextInput(attrs={'class': 'form-control'}),
            'qtd': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'preco': forms.DecimalField(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class MovimentacaoForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Saida', 'Saída'),
        ('Devolucao', 'Devolução'),
    ]
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    qtd = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}))
    motivo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    empreendimento = forms.ModelChoiceField(queryset=Empreendimento.objects.all(), required=False,
                                            widget=forms.Select(attrs={'class': 'form-control'}),
                                            empty_label='Selecione...')
    quadra = forms.ModelChoiceField(queryset=Quadra.objects.none(), required=False,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    empty_label='Selecione...')
    lote = forms.ModelChoiceField(queryset=Lote.objects.none(), required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}),
                                  empty_label='Selecione...')

    class Meta:
        model = Movimentacao
        fields = ['qtd', 'tipo', 'motivo', 'empreendimento', 'quadra', 'lote']
        exclude = ['produto']  # Será setado na view

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializa quadra e lote vazios (preenchidos via JS)
        self.fields['quadra'].queryset = Quadra.objects.none()
        self.fields['lote'].queryset = Lote.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        qtd = cleaned_data.get('qtd')

        if qtd <= 0:
            raise ValidationError('Quantidade deve ser um número positivo.')

        if tipo in ['Saida', 'Devolucao']:
            if not cleaned_data.get('empreendimento'):
                raise ValidationError('Empreendimento é obrigatório para Saída ou Devolução.')
            if not cleaned_data.get('quadra'):
                raise ValidationError('Quadra é obrigatória para Saída ou Devolução.')
            if not cleaned_data.get('lote'):
                raise ValidationError('Lote é obrigatório para Saída ou Devolução.')

        return cleaned_data
