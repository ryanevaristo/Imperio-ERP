from django.db import models
from uuid import uuid4
from produto.models import Lote
from django.core.exceptions import ValidationError

# Create your models here.

class Produtos(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,default=uuid4)
    produto = models.CharField(max_length=100, null=True, blank=True)
    qtd = models.IntegerField(default=0, null=True, blank=True)
    qtd_min = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    custo = models.DecimalField(default=0, null=True, blank=True, decimal_places=2, max_digits=10)
    # Margem = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    # venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey('EstoqueCategoria', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    def __str__(self):
        return self.produto
    
  
    # def margem_porcentagem(self):
    #     if self.custo > 0:
    #         return (self.Margem / self.custo) * 100
    #     return 0
    

class EstoqueCategoria(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    nome_categoria = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_categoria
    

class Movimentacao(models.Model):

    CHOICE_TIPO = (
        ('Entrada', 'Entrada'),
        ('Saida', 'Saída'),
        ('Devolucao', 'Devolução')
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    produto = models.ForeignKey('Produtos',on_delete=models.CASCADE, related_name='movimentacoes')
    qtd = models.IntegerField(default=0, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=CHOICE_TIPO, null=True, blank=True)
    motivo = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    empreendimento = models.ForeignKey('produto.Empreendimento', on_delete=models.CASCADE, null=True, blank=True)
    quadra = models.ForeignKey('produto.Quadra', on_delete=models.CASCADE, null=True, blank=True)

    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True, related_name='lote')

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'

    def clean(self):
        if self.tipo == 'saida' and not self.lote:
            raise ValidationError("Movimentações de saída devem estar vinculadas a um lote.")
    
    def __str__(self):
        return f'{self.produto} - {self.tipo} - {self.qtd}'
    

class Notificacao(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)  # Para marcar se o usuário já viu a notificação

    def __str__(self):
        return f'Notificação: {self.produto.produto} - {self.mensagem[:20]}'

    
