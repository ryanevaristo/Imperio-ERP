from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from estoque.models  import Notificacao
from core.models import NotificacoesGeral
from notifications.models import Notification


@receiver(post_save, sender=Notificacao)
def criar_notificacao_estoque(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            empresa=instance.empresa,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            mensagem=instance.mensagem,
            criado_em=instance.data_criacao,
            visualizado=instance.visualizado
        )


@receiver(post_save, sender=NotificacoesGeral)
def criar_notificacao_geral(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            empresa=instance.empresa,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            mensagem=instance.mensagem,
            criado_em=instance.criado_em,
            visualizado=instance.visualizado
        )

@receiver(post_save, sender=Notification)
def  sync_visualizado_status(sender, instance, **kwargs):
    try:
        source = instance.content_type.get_object_for_this_type(id=instance.object_id)
        if hasattr(source, 'visualizado') and source.visualizado != instance.visualizado:
            source.visualizado = instance.visualizado
            source.save(update_fields=['visualizado'])
    except Exception:
        pass