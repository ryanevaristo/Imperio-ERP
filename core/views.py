from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from rolepermissions.decorators import has_role_decorator
from .models import Empresa, NotificacoesGeral
from notifications.models import Notification
from datetime import date, timedelta
from functools import wraps


def superuser_required(view_func):
    """Decorator: exige is_superuser. Redireciona para login se não autenticado."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/auth/login/')
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

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


@superuser_required
def superuser_dashboard(request):
    """Painel do dono do sistema: lista todas as empresas com status de assinatura."""
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')

    empresas = Empresa.objects.all().order_by('nome')

    if q:
        empresas = empresas.filter(nome__icontains=q)

    hoje = date.today()

    # Anota status de cada empresa para uso no template
    rows = []
    for emp in empresas:
        dias = emp.dias_para_vencimento()
        if not emp.mensalidade_ativa:
            status = 'inativa'
        elif emp.mensalidade_vencida():
            status = 'vencida'
        elif dias is not None and dias <= 7:
            status = 'alerta'
        else:
            status = 'ativa'

        if status_filter and status != status_filter:
            continue

        rows.append({
            'empresa': emp,
            'status': status,
            'dias': dias,
        })

    # Contadores para os cards
    totais = {
        'total': len(rows),
        'ativas': sum(1 for r in rows if r['status'] == 'ativa'),
        'alerta': sum(1 for r in rows if r['status'] == 'alerta'),
        'vencidas': sum(1 for r in rows if r['status'] == 'vencida'),
        'inativas': sum(1 for r in rows if r['status'] == 'inativa'),
    }

    return render(request, 'superuser/dashboard.html', {
        'rows': rows,
        'totais': totais,
        'q': q,
        'status_filter': status_filter,
        'hoje': hoje,
    })


@superuser_required
@require_POST
def superuser_toggle_ativo(request, empresa_id):
    """Ativa ou desativa a mensalidade de uma empresa."""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.mensalidade_ativa = not empresa.mensalidade_ativa
    empresa.save(update_fields=['mensalidade_ativa'])
    status = 'ativada' if empresa.mensalidade_ativa else 'desativada'
    messages.success(request, f'Assinatura de "{empresa.nome}" {status} com sucesso.')
    return redirect('superuser_dashboard')


@superuser_required
@require_POST
def superuser_renovar(request, empresa_id):
    """Renova a assinatura da empresa por N dias a partir de hoje (ou do vencimento atual)."""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    dias = int(request.POST.get('dias', 30))

    base = max(empresa.data_vencimento_mensalidade or date.today(), date.today())
    nova_data = base + timedelta(days=dias)

    empresa.data_vencimento_mensalidade = nova_data
    empresa.mensalidade_ativa = True
    empresa.save(update_fields=['data_vencimento_mensalidade', 'mensalidade_ativa'])

    messages.success(
        request,
        f'Assinatura de "{empresa.nome}" renovada até {nova_data.strftime("%d/%m/%Y")}.'
    )
    return redirect('superuser_dashboard')


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
