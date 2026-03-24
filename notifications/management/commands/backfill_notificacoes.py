from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from estoque.models import Notificacao
from core.models import NotificacoesGeral
from notifications.models import Notification


class Command(BaseCommand):
    help = 'Backfill existing notifications into the Notification model'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando o backfill de notificações...')

        # Backfill Notificacao instances
        notificacoes = Notificacao.objects.all()
        for notificacao in notificacoes:
            Notification.objects.get_or_create(
                empresa=notificacao.empresa,
                content_type=ContentType.objects.get_for_model(Notificacao),
                object_id=notificacao.id,
                defaults={
                    'mensagem': notificacao.mensagem,
                    'criado_em': notificacao.data_criacao,
                    'visualizado': notificacao.visualizado
                }
            )
        self.stdout.write(f'Backfill de {notificacoes.count()} notificações de estoque concluído.')

        # Backfill NotificacoesGeral instances
        notificacoes_gerais = NotificacoesGeral.objects.all()
        for notificacao_geral in notificacoes_gerais:
            Notification.objects.get_or_create(
                empresa=notificacao_geral.empresa,
                content_type=ContentType.objects.get_for_model(NotificacoesGeral),
                object_id=notificacao_geral.id,
                defaults={
                    'mensagem': notificacao_geral.mensagem,
                    'criado_em': notificacao_geral.criado_em,
                    'visualizado': notificacao_geral.visualizado
                }
            )
        self.stdout.write(f'Backfill de {notificacoes_gerais.count()} notificações gerais concluído.')

        self.stdout.write('Backfill de notificações concluído com sucesso.')