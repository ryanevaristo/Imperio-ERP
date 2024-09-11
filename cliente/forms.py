from .models import Cliente

from django import forms


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_completo': 'Nome Completo',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'cpf_cnpj': 'CPF/CNPJ',
            'endereco': 'Endereço',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'cep': 'CEP',
        }

        def cpf_cnpj_validator(value):
            if len(value) == 11 and value.contains('.') and value.contains('-'):
                if not value.isdigit():
                    raise forms.ValidationError('CPF inválido')
            elif len(value) == 14 and value.contains('.') and value.contains('-') and value.contains('/'):
                if not value.isdigit():
                    raise forms.ValidationError('CNPJ inválido')
            else:
                raise forms.ValidationError('CPF/CNPJ inválido')
            return value
        
        def clean_cpf_cnpj(self):
            cpf_cnpj = self.cleaned_data['cpf_cnpj']
            return self.cpf_cnpj_validator(cpf_cnpj)