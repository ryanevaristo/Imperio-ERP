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
    status_venda = models.CharField(max_length=10, choices=CHOICE_STATUS_VENDA, default='Pendente')
    quitado = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-create_at']
        indexes = [
            models.Index(fields=['empresa', 'status_venda']),
            models.Index(fields=['empresa', 'create_at']),
        ]

    def __str__(self):
        return f'Venda {str(self.id_venda)[:8]} - {self.id_cliente}'

    def total_pago(self):
        return sum(p.valor for p in self.pagamento_set.all())

    def saldo_restante(self):
        return self.valor_venda - self.total_pago()

    def get_data_venda(self):
        return self.data_venda.strftime('%d/%m/%Y')


class Pagamento(models.Model):

    CHOICE_FORMA_PAGAMENTO = (
        ('Dinheiro', 'Dinheiro'),
        ('Cartão de Crédito', 'Cartão de Crédito'),
        ('Pix', 'Pix'),
        ('Boleto', 'Boleto'),
        ('Transferência', 'Transferência'),
    )

    id_venda = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    forma_pagamento = models.CharField(max_length=20, choices=CHOICE_FORMA_PAGAMENTO)
    data_pagamento = models.DateField(default=timezone.now)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_pagamento']

    def __str__(self):
        return f'Pagamento R${self.valor} - {self.forma_pagamento}'




