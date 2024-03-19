from django.db import models


class ContaPagar(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao
    
    def get_valor(self):
        return "R$ " + str(self.valor).replace('.', ',')
    
    def get_data_vencimento(self):
        return self.data_vencimento.strftime('%d/%m/%Y')
# Create your models here.
