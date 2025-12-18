from datetime import datetime
from django.db import models
from uuid import uuid4
from django.utils import timezone
from cliente.models import  Cliente
from core.models import Empresa


# Create your models here.

class Empreendimento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    imagem = models.ImageField(upload_to='empreendimentos/', blank=True, null=True, default='empreendimentos/default.png')
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    localizacao = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

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
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name = 'Quadra'
        verbose_name_plural = 'Quadras'

    def __str__(self):
        return self.nome
    def get_total_lotes_disponiveis(self):
        return self.lote_set.filter(status='D').count()
    
    def get_total_lotes_vendidos(self):
        return self.lote_set.filter(status='V').count()
    
    def  lotes_disponiveis(self):
        return self.lote_set.filter(status='D')
    
    def lotes_vendidos(self):
        return self.lote_set.filter(status="V")
    
    
    

class Lote(models.Model):
    CHOICE_STATUS ={
        ('D', 'Disponível'),
        ('V', 'Vendido'),
        ('R', 'Reservado'),
    }
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    numero = models.IntegerField(auto_created=True)
    metragem = models.CharField(max_length=10)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_aquisicao = models.DateField(null=True, blank=True, default=datetime(1900, 1, 1))
    status = models.CharField(max_length=1, default=True, choices=CHOICE_STATUS)
    proprietario = models.ForeignKey(Cliente, blank=True, null=True, related_name="Lotes", on_delete=models.CASCADE)
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'

    def __str__(self):
        return f'{self.quadra} - {self.numero}'
    
    def  get_data_aquisicao(self):
        return self.data_aquisicao.strftime('%d/%m/%Y')

