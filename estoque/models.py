from django.db import models

# Create your models here.

class Produtos(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    nome = models.CharField(max_length=100)
    qtd = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    def __str__(self):
        return self.nome
    

class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    nome_categoria = models.CharField(max_length=100)
    produto = models.ForeignKey('Produtos', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_categoria
    