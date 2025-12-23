from django.db import models
from uuid import uuid4
from django.utils import timezone
from datetime import date

class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    nome = models.CharField(max_length=255, unique=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Campos de Mensalidade
    data_vencimento_mensalidade = models.DateField(
        verbose_name='Data de Vencimento da Mensalidade',
        null=True,
        blank=True,
        help_text='Data em que a mensalidade vence'
    )
    mensalidade_ativa = models.BooleanField(
        verbose_name='Mensalidade Ativa',
        default=True,
        help_text='Indica se a mensalidade está ativa'
    )
    mensalidade_valor = models.DecimalField(
        verbose_name='Valor da Mensalidade',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor mensal da assinatura'
    )
    mensalidade_dia_vencimento = models.IntegerField(
        verbose_name='Dia do Vencimento',
        null=True,
        blank=True,
        help_text='Dia do mês para vencimento (1-31)'
    )

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cnpj']),
            models.Index(fields=['created_at']),
            models.Index(fields=['data_vencimento_mensalidade']),
        ]

    def __str__(self):
        return self.nome
    
    def mensalidade_vencida(self):
        """Verifica se a mensalidade está vencida"""
        if not self.mensalidade_ativa:
            return True
        if self.data_vencimento_mensalidade is None:
            return False
        return date.today() > self.data_vencimento_mensalidade
    
    def pode_acessar_sistema(self):
        """Verifica se a empresa pode acessar o sistema"""
        return self.mensalidade_ativa and not self.mensalidade_vencida()
    

