from django.db import models
from datetime import datetime


class ContaPagar(models.Model):

    choice_forma_pagamento = (
        ('D', 'Dinheiro'),
        ('C', 'Cartão de Crédito'),
        ('B', 'Boleto'),
        ('T', 'Transferência Bancária'),
        ('C', 'Cheque'),
        ('P', 'PIX')
    )

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    data_pagamento = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    forma_pagamento = models.CharField(max_length=1, choices=choice_forma_pagamento,default='D',null=True, blank=True)
    categoria = models.ForeignKey('DespesasCategoria', on_delete=models.CASCADE, null=True, blank=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_vencimento(self):
        return self.data_vencimento.strftime('%d/%m/%Y')
    
    def get_data_pagamento(self):
        return self.data_pagamento.strftime('%d/%m/%Y')
    def edit_data_vencimento(self):
        return self.data_vencimento.strftime('%Y-%m-%d')
    def edit_data_pagamento(self):
        return self.data_pagamento.strftime('%Y-%m-%d')
    def data_pagamento_mês_atual(self):
        return self.data_pagamento.strftime('%m')
    

class DespesasCategoria(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao

class ContaReceber(models.Model):
    choice_forma_recebimento = (
        ('D', 'Dinheiro'),
        ('E', 'Cartão de Crédito'),
        ('B', 'Boleto'),
        ('T', 'Transferência Bancária'),
        ('C', 'Cheque')
    )
    cliente = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    data_recebimento = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    recebido = models.BooleanField(default=False)
    forma_recebimento = models.CharField(max_length=1, choices=choice_forma_recebimento,default='D',null=True, blank=True)

    def __str__(self):
        return self.descricao
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_vencimento(self):
        return self.data_vencimento.strftime('%d/%m/%Y')
    def get_data_recebimento(self):
        return self.data_recebimento.strftime('%d/%m/%Y')
    def edit_data_vencimento(self):
        return self.data_vencimento.strftime('%Y-%m-%d')
    def edit_data_recebimento(self):
        return self.data_recebimento.strftime('%Y-%m-%d')
    
class Cheque(models.Model):
    choice_situacao = (
        ('E', 'Emitido'),
        ('C', 'Compensado'),
        ('V', 'Vencido'),
        ('S', 'Sem Fundo'),
        ('D', 'Devolvido')
    )
    choice_banco = (
        ('001', 'Banco do Brasil'),
        ('104', 'Caixa Econômica Federal'),
        ('237', 'Bradesco'),
        ('341', 'Itaú'),
        ('356', 'Santander'),
        ('033', 'Banco Santander (Brasil)'),
        ('745', 'Citibank'),
        ('399', 'HSBC'),
        ('422', 'Safra'),
        ('389', 'Mercantil do Brasil'),
        ('633', 'Rendimento'),
        ('652', 'Itaú Unibanco Holding'),
        ('745', 'Banco Citibank'),
        ('748', 'Sicredi'),
        ('756', 'Sicoob')
    )
    numero = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nome_titular = models.CharField(max_length=100)
    nome_repassador = models.CharField(max_length=100, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    banco = models.CharField(max_length=3, choices=choice_banco, default='001',null=True, blank=True)
    data_compensacao = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    situacao = models.CharField(max_length=1, choices=choice_situacao,default='E',null=True, blank=True)

    def __str__(self):
        return self.nome_titular
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_compensacao(self):
        return self.data_compensacao.strftime('%d/%m/%Y')
    
    

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return self.nome
# Create your models here.
