from django.db import models


class ContaPagar(models.Model):

    choice_forma_pagamento = (
        ('D', 'Dinheiro'),
        ('C', 'Cartão de Crédito'),
        ('B', 'Boleto'),
        ('T', 'Transferência Bancária'),
        ('C', 'Cheque')
    )

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    forma_pagamento = models.CharField(max_length=1, choices=choice_forma_pagamento,default='D',null=True, blank=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_vencimento(self):
        return self.data_vencimento.strftime('%d/%m/%Y')
    

class ContaReceber(models.Model):
    choice_forma_recebimento = (
        ('D', 'Dinheiro'),
        ('C', 'Cartão de Crédito'),
        ('B', 'Boleto'),
        ('T', 'Transferência Bancária'),
        ('C', 'Cheque')
    )
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_recebimento = models.DateField(null=True, blank=True)
    recebido = models.BooleanField(default=False)
    forma_recebimento = models.CharField(max_length=1, choices=choice_forma_recebimento,default='D',null=True, blank=True)

    def __str__(self):
        return self.descricao
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_vencimento(self):
        return self.data_vencimento.strftime('%d/%m/%Y')
    
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
    numero = models.CharField(max_length=20)
    nome_titular = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    banco = models.CharField(max_length=3, choices=choice_banco)
    data_emissao = models.DateField()
    data_compensacao = models.DateField(null=True, blank=True)
    situacao = models.CharField(max_length=1, choices=choice_situacao,default='E',null=True, blank=True)

    def __str__(self):
        return self.numero
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_emissao(self):
        return self.data_emissao.strftime('%d/%m/%Y')
    
    def get_data_compensacao(self):
        return self.data_compensacao.strftime('%d/%m/%Y')
    
    
# Create your models here.
