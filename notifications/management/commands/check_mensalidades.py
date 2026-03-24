# notifications/management/commands/check_mensalidades.py
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from datetime import date
from core.models import Empresa
from notifications.models import Notification

class Command(BaseCommand):
    help = "Cria notificações para mensalidades que vencem hoje"

    def handle(self, *args, **options):
        hoje = date.today()

        # Empresas com data exata de vencimento
        vencendo_por_data = Empresa.objects.filter(
            mensalidade_ativa=True,
            data_vencimento_mensalidade=hoje
        )

        # Empresas com dia fixo de vencimento
        vencendo_por_dia = Empresa.objects.filter(
            mensalidade_ativa=True,
            mensalidade_dia_vencimento=hoje.day
        )

        ct = ContentType.objects.get_for_model(Empresa)
        total = 0

        for empresa in list(vencendo_por_data) + list(vencendo_por_dia):
            if not Notification.objects.filter(content_type=ct, object_id=empresa.pk, mensagem__icontains="Mensalidade vence").exists():
                Notification.objects.create(
                    empresa=empresa,
                    content_type=ct,
                    object_id=empresa.pk,
                    mensagem=f"Mensalidade vence hoje ({empresa.mensalidade_valor} R$)",
                    visualizado=False
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f"{total} notificações de vencimento criadas"))