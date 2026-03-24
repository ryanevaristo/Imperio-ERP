from django.contrib import admin

# Register your models here.

from .models import Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'mensagem', 'visualizado', 'criado_em')
    list_filter = ('visualizado', 'criado_em')
    search_fields = ('mensagem', 'empresa__nome')
    
