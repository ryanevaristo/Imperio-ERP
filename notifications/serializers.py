from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    source_model = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'mensagem', 'criado_em', 'visualizado', 'source_model']

    def get_source_model(self, obj):
        return obj.content_type.model