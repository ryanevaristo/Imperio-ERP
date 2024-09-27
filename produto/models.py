from django.db import models
from uuid import uuid4
from django.utils import timezone

# Create your models here.

class Empreendimento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    imagem = models.ImageField(upload_to='empreendimentos/', blank=True, null=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    localizacao = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Empreendimento'
        verbose_name_plural = 'Empreendimentos'

    def __str__(self):
        return self.nome
    

class Quadra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    imagem = models.ImageField(upload_to='quadras/', blank=True, null=True)
    empreendimento = models.ForeignKey(Empreendimento, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    metragem = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        verbose_name = 'Quadra'
        verbose_name_plural = 'Quadras'

    def __str__(self):
        return self.nome
    
    

class Lote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)
    numero = models.IntegerField()
    metragem = models.DecimalField(max_digits=10, decimal_places=2)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    proprietario = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'

    def __str__(self):
        return f'{self.quadra} - {self.numero}'

