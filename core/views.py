from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from .models import Empresa, NotificacoesGeral
from notifications.models import Notification

# Create your views here.   


@login_required(login_url='/auth/login/')
def home(request):
    empresa = request.user.empresa
    notificacoes =Notification.objects.filter(empresa=empresa, visualizado=False).order_by('-criado_em')[:20]
    return render(request, 'home.html', {'notificacoes': notificacoes})
    


def error_403_view(request, exception):
    return render(request, '403.html', status=403)


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
