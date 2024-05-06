from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    choice_cargo = (
        ('A', 'Administrador'),
        ('U', 'Usuario'),
        ('V','vendedor')
    )
    cargo = models.CharField(max_length=1, choices=choice_cargo, default='user')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return self.username
    

