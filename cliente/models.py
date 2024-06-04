from django.db import models

# Create your models here.

class Cliente(models.Model):
    nome_completo = models.CharField(max_length=100, blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo
        
    
    