from django.db import models

# Create your models here.

class Cliente(models.Model):
    nome_completo = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=20)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo
        
    
    