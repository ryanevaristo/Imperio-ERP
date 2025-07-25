from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    choice_cargo = (
        ('A', 'Administrador'),
        ('V', 'Vendedor'),
        ('G','Gerente'),
        ('E', 'Estoquista'),
    )
    cargo = models.CharField(max_length=1, choices=choice_cargo, default='V')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return self.username
    
    def get_cargo_display(self):
        for cargo in self.choice_cargo:
            if cargo[0] == self.cargo:
                return cargo[1]
        return None
    

