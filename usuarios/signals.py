from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Users
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role


@receiver(post_save, sender=Users)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.cargo == "G":
            assign_role(instance, 'gerente')
        elif instance.cargo == 'A':
            assign_role(instance, 'administrador')
        elif instance.cargo == 'V':
            assign_role(instance, 'vendedor')
    else:
        if instance.cargo == "G" and not has_role(instance, 'gerente'):
            assign_role(instance, 'gerente')
        elif instance.cargo == 'A' and not has_role(instance, 'administrador'):
            assign_role(instance, 'administrador')
        elif instance.cargo == 'V' and not has_role(instance, 'vendedor'):
            assign_role(instance, 'vendedor')