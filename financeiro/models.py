from django.db import models
from datetime import datetime
from cliente.models import Cliente
from core.models import Empresa


class ContaPagar(models.Model):

    choice_forma_pagamento = (
        ('D', 'Dinheiro'),
        ('B', 'Boleto'),
        ('T', 'Banco'),
        ('C', 'Cheque'),
        ('P', 'PIX'),
        ('M',"Dinheiro/Banco"),
        ("N","Cheque/Dinheiro")
    )

    descricao = models.CharField(max_length=1000)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    forma_pagamento = models.CharField(max_length=1, choices=choice_forma_pagamento,default='D',null=True, blank=True)
    categoria = models.ForeignKey('DespesasCategoria', on_delete=models.SET_NULL , null=True, blank=True)
    pago = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.descricao
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    
    def get_data_pagamento(self):
        return self.data_pagamento.strftime('%d/%m/%Y')
    def edit_data_pagamento(self):
        return self.data_pagamento.strftime('%Y-%m-%d')
    def data_pagamento_mês_atual(self):
        return self.data_pagamento.strftime('%m')
    

class DespesasCategoria(models.Model):
    nome_categoria = models.CharField(max_length=100)
    conta_pagar = models.ForeignKey('ContaPagar', on_delete=models.SET_NULL, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome_categoria

class ContaReceber(models.Model):
    choice_forma_recebimento = (
        ('D', 'Dinheiro'),
        ('B', 'Boleto'),
        ('E', 'Cartão'),
        ('T', 'Banco'),
        ('C', 'Cheque'),
        ('P', 'PIX'),
        ('M',"Dinheiro/Banco"),
        ("N","Cheque/Dinheiro")
    )
    cliente = models.ForeignKey(Cliente,on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.TextField(max_length=1000,null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_recebimento = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    recebido = models.BooleanField(default=False)
    forma_recebimento = models.CharField(max_length=1, choices=choice_forma_recebimento,default='D',null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['empresa', 'data_recebimento']),
            models.Index(fields=['empresa', 'recebido']),
            models.Index(fields=['empresa', 'cliente']),
            models.Index(fields=['cliente']),
        ]

    def __str__(self):
        return self.descricao
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    def get_data_recebimento(self):
        return self.data_recebimento.strftime('%d/%m/%Y')
    def edit_data_recebimento(self):
        return self.data_recebimento.strftime('%Y-%m-%d')
    
    
class Cheque(models.Model):
    choice_situacao = (
        ('E', 'Emitido'),
        ('C', 'Compensado'),
        ("G", 'Vencido'),
        ('S', 'Sem Fundo'),
        ('D', 'Devolvido'),
        ('R', 'Repassado')
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
    nome_titular = models.ForeignKey(Cliente, null=True,on_delete=models.SET_NULL , blank=True)
    nome_repassador = models.CharField(max_length=100, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    banco = models.CharField(max_length=3, choices=choice_banco, default='001',null=True, blank=True)
    data_compensacao = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    situacao = models.CharField(max_length=1, choices=choice_situacao,default='E',null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.numero
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_compensacao(self):
        return self.data_compensacao.strftime('%d/%m/%Y')
    
    def edit_data_compensacao(self):
        return self.data_compensacao.strftime('%Y-%m-%d')
    
    

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome
# Create your models here.
