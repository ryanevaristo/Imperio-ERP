from django.db import models
from uuid import uuid4

# Create your models here.

class Produtos(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,default=uuid4)
    produto = models.CharField(max_length=100, null=True, blank=True)
    qtd = models.IntegerField(default=0, null=True, blank=True)
    qtd_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custo = models.IntegerField(default=0, null=True, blank=True)
    Margem = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey('EstoqueCategoria', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    def __str__(self):
        return self.produto
    
  
    def margem_porcentagem(self):
        if self.custo > 0:
            return (self.Margem / self.custo) * 100
        return 0
    

class EstoqueCategoria(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    nome_categoria = models.CharField(max_length=100)
    def __str__(self):
        return self.nome_categoria
    

class Movimentacao(models.Model):

    CHOICE_TIPO = (
        ('Entrada', 'Entrada'),
        ('Saída', 'Saída'),
        ('Devolução', 'Devolução')
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, null=True, blank=True)
    qtd = models.IntegerField(default=0, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=CHOICE_TIPO, null=True, blank=True)
    motivo = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
    
    def __str__(self):
        return self.produto.produto