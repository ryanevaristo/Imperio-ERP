from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import Empresa  # ajuste conforme seu projeto

class Notification(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='notifications')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['empresa', 'visualizado']),
            models.Index(fields=['empresa', 'criado_em']),
            models.Index(fields=['content_type', 'object_id']),
        ]
        ordering = ['-criado_em']

    def __str__(self):
        return f'Notification {self.id} for {self.empresa} - {self.mensagem[:40]}'