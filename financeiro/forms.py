from .models import Cheque,ContaPagar,ContaReceber,DespesasCategoria
from django import forms

class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = ['descricao', 'valor', 'data_pagamento', 'forma_pagamento', 'categoria', 'pago']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'pago': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor',
            'data_pagamento': 'Data de Pagamento',
            'forma_pagamento': 'Forma de Pagamento',
            'categoria': 'Categoria',
            'pago': 'Pago',
        }
    

class DespesasCategoriaForm(forms.ModelForm):
    class Meta:
        model = DespesasCategoria
        fields = ['nome_categoria']
        widgets = {
            'nome_categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_categoria': 'Nome da Categoria',
        }

class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['cliente', 'descricao', 'valor', 'data_recebimento', 'forma_recebimento', 'recebido']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'data_recebimento': forms.DateInput(attrs={'class': 'form-control'}),
            'forma_recebimento': forms.Select(attrs={'class': 'form-control'}),
            'recebido': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cliente': 'Cliente',
            'descricao': 'Descrição',
            'valor': 'Valor',
            'data_recebimento': 'Data de Recebimento',
            'forma_recebimento': 'Forma de Recebimento',
            'recebido': 'Recebido',
        }