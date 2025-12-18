from django.db import models
from uuid import uuid4

class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    nome = models.CharField(max_length=255, unique=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cnpj']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.nome
    

