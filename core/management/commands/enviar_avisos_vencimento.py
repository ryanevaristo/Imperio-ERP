"""
Envia e-mails de aviso de vencimento de mensalidade para empresas
cujo vencimento está em exatamente 7, 3 ou 1 dia(s).

Uso:
    python manage.py enviar_avisos_vencimento
    python manage.py enviar_avisos_vencimento --dry-run   # apenas lista, não envia

Configurar no cron (ex: todo dia às 8h):
    0 8 * * * cd /app && python manage.py enviar_avisos_vencimento >> /var/log/avisos.log 2>&1
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from core.models import Empresa
from usuarios.models import Users
from datetime import date, timedelta


DIAS_AVISO = [7, 3, 1]  # D-7, D-3, D-1


def _destinatarios(empresa):
    """Retorna lista de e-mails dos admins ativos da empresa."""
    admins = Users.objects.filter(
        empresa=empresa,
        cargo='A',
        is_active=True,
    ).exclude(email='').values_list('email', flat=True)
    # Inclui também o e-mail cadastrado na empresa
    emails = list(admins)
    if empresa.email and empresa.email not in emails:
        emails.append(empresa.email)
    return emails


def _enviar_aviso(empresa, dias, dry_run=False):
    """Monta e envia (ou simula) o e-mail de aviso."""
    destinatarios = _destinatarios(empresa)
    if not destinatarios:
        return 0

    data_fmt = empresa.data_vencimento_mensalidade.strftime('%d/%m/%Y')

    if dias == 1:
        urgencia = 'URGENTE — Sua assinatura vence amanhã!'
        intro = 'Sua assinatura do Imperio ERP vence <strong>amanhã</strong>.'
    elif dias <= 3:
        urgencia = f'Sua assinatura vence em {dias} dias'
        intro = f'Sua assinatura do Imperio ERP vence em <strong>{dias} dias</strong> ({data_fmt}).'
    else:
        urgencia = f'Lembrete: assinatura vence em {dias} dias'
        intro = f'Este é um lembrete de que sua assinatura vence em <strong>{dias} dias</strong> ({data_fmt}).'

    assunto = f'[Imperio ERP] {urgencia}'

    mensagem_txt = (
        f'Olá, equipe {empresa.nome}!\n\n'
        f'{urgencia}\n\n'
        f'Vencimento: {data_fmt}\n\n'
        f'Para renovar, entre em contato com o suporte:\n'
        f'WhatsApp: (62) 99999-0000\n'
        f'E-mail: suporte@imperioerp.com.br\n\n'
        f'Equipe Imperio ERP'
    )

    if dry_run:
        return len(destinatarios)

    try:
        send_mail(
            subject=assunto,
            message=mensagem_txt,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=destinatarios,
            fail_silently=False,
        )
        return len(destinatarios)
    except Exception as e:
        raise RuntimeError(f'Falha ao enviar e-mail para {empresa.nome}: {e}')


class Command(BaseCommand):
    help = 'Envia avisos de vencimento de mensalidade (D-7, D-3, D-1)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Lista empresas que receberiam aviso sem enviar e-mails.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        hoje = date.today()

        if dry_run:
            self.stdout.write(self.style.WARNING('=== DRY RUN — nenhum e-mail será enviado ==='))

        total_enviados = 0
        total_erros = 0

        for dias in DIAS_AVISO:
            data_alvo = hoje + timedelta(days=dias)

            empresas = Empresa.objects.filter(
                mensalidade_ativa=True,
                data_vencimento_mensalidade=data_alvo,
            )

            if not empresas.exists():
                self.stdout.write(f'D-{dias}: nenhuma empresa.')
                continue

            for empresa in empresas:
                try:
                    qtd = _enviar_aviso(empresa, dias, dry_run=dry_run)
                    acao = 'simularia envio' if dry_run else 'enviado'
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'D-{dias} | {empresa.nome} | {acao} para {qtd} destinatário(s)'
                        )
                    )
                    total_enviados += 1
                except RuntimeError as e:
                    self.stdout.write(self.style.ERROR(str(e)))
                    total_erros += 1

        self.stdout.write('─' * 50)
        self.stdout.write(
            self.style.SUCCESS(f'Concluído: {total_enviados} aviso(s) | {total_erros} erro(s)')
        )
