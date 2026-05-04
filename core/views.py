from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from .models import Empresa, NotificacoesGeral
from notifications.models import Notification
from datetime import date

# Create your views here.   


@login_required(login_url='/auth/login/')
def home(request):
    empresa = request.user.empresa
    notificacoes =Notification.objects.filter(empresa=empresa, visualizado=False).order_by('-criado_em')[:20]
    return render(request, 'home.html', {'notificacoes': notificacoes})
    


def landing(request):
    return render(request, 'landing.html')


def error_403_view(request, exception):
    return render(request, '403.html', status=403)


@login_required(login_url='/auth/login/')
@has_role_decorator('administrador')
def minha_assinatura(request):
    empresa = request.user.empresa
    hoje = date.today()

    # Status da assinatura
    dias = empresa.dias_para_vencimento()
    vencida = empresa.mensalidade_vencida()
    ativa = empresa.mensalidade_ativa

    if not ativa:
        status = 'inativa'
        status_label = 'Inativa'
    elif vencida:
        status = 'vencida'
        status_label = 'Vencida'
    elif dias is not None and dias <= 7:
        status = 'alerta'
        status_label = f'Vence em {dias} dia{"s" if dias != 1 else ""}'
    else:
        status = 'ativa'
        status_label = 'Ativa'

    # Histórico de notificações de mensalidade
    notificacoes = NotificacoesGeral.objects.filter(
        empresa=empresa
    ).order_by('-criado_em')[:20]

    context = {
        'empresa': empresa,
        'status': status,
        'status_label': status_label,
        'dias': dias,
        'vencida': vencida,
        'hoje': hoje,
        'notificacoes': notificacoes,
    }
    return render(request, 'minha_assinatura.html', context)


@login_required(login_url='/auth/login/')
def notificacao_vencimento_mensalidade(request):
    if request.user.is_authenticated:
        empresa = request.user.empresa
        notificacoes = NotificacoesGeral.objects.filter(empresa=empresa, visualizado=False)
        if empresa.dias_para_vencimento() is not None and empresa.dias_para_vencimento() <= 5:
            message = f'Sua mensalidade vence em {empresa.dias_para_vencimento()} dias.'
            NotificacoesGeral.objects.create(
                empresa=empresa,
                mensagem=message
            )
        return render(request, 'notificacoes_vencimento.html', {'notificacoes': notificacoes})
    return render(request, 'notificacoes_vencimento.html', {'notificacoes': []})
