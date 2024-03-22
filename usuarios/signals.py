from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Users
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role


@receiver(post_save, sender=Users)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.cargo == 'V':
            assign_role(instance, 'vendedor')
        elif instance.cargo == 'A':
            assign_role(instance, 'administrador')
        elif instance.cargo == 'U':
            assign_role(instance, 'usuario')
    else:
        if instance.cargo == 'V' and not has_role(instance, 'vendedor'):
            assign_role(instance, 'vendedor')
        elif instance.cargo == 'A' and not has_role(instance, 'administrador'):
            assign_role(instance, 'administrador')
        elif instance.cargo == 'U' and not has_role(instance, 'usuario'):
            assign_role(instance, 'usuario')