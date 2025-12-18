from django.db import models
from uuid import uuid4
from django.utils import timezone
from produto.models import Lote
from cliente.models import Cliente
from core.models import Empresa

# Create your models here.

class Vendas(models.Model):
    
    CHOICE_STATUS_VENDA = (
        ('Pendente', 'Pendente'),
        ('Concluída', 'Concluída'),
        ('Cancelada', 'Cancelada')
    )

    id_venda = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id_lote  = models.ForeignKey(Lote, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(default=timezone.now)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    status_venda =  models.CharField(max_length=10, choices=CHOICE_STATUS_VENDA, default='Pendente')
    quitado =  models.BooleanField(default=False)
    create_at  = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
    
    def  __str__(self):
        return self.id_venda

class  Pagamento(models.Model):

    CHOICE_FORMA_PAGAMENTO  = (
        ('Dinheiro', 'Dinheiro'),
        ('Cartão de Crédito', 'Cartão de Crédito'),
        ("Pix",  "Pix"),
        ("Boleto", "Boleto"),
        )
    
    id_venda  = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    forma_pagamento = models.CharField(max_length=20, choices=CHOICE_FORMA_PAGAMENTO)
    data_pagamento = models.DateField(auto_now_add=True)
    valor =  models.DecimalField(max_digits=10, decimal_places=2)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"




