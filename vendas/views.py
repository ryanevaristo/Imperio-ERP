from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from rolepermissions.decorators import has_role_decorator

from .models import Vendas, Pagamento
from cliente.models import Cliente
from produto.models import Lote
from global_variables import lista_permissoes_vendas


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_vendas)
def home_vendas(request):
    vendas = Vendas.objects.filter(empresa=request.user.empresa).select_related(
        'id_cliente', 'id_lote', 'id_lote__quadra'
    )

    status_filtro = request.GET.get('status')
    if status_filtro:
        vendas = vendas.filter(status_venda=status_filtro)

    pesquisar = request.GET.get('pesquisar')
    if pesquisar:
        vendas = vendas.filter(id_cliente__nome_completo__icontains=pesquisar)

    paginator = Paginator(vendas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vendas/vendas.html', {
        'page_obj': page_obj,
        'pesquisar': pesquisar,
        'status_filtro': status_filtro,
    })


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_vendas)
def cadastrar_venda(request):
    if request.method == 'GET':
        clientes = Cliente.objects.filter(empresa=request.user.empresa)
        lotes = Lote.objects.filter(empresa=request.user.empresa, status='D').select_related('quadra')
        return render(request, 'vendas/cadastrar_venda.html', {
            'clientes': clientes,
            'lotes': lotes,
        })

    with transaction.atomic():
        id_cliente = request.POST.get('cliente')
        id_lote = request.POST.get('lote')
        valor_venda = request.POST.get('valor_venda')
        forma_pagamento = request.POST.get('forma_pagamento')
        valor_entrada = request.POST.get('valor_entrada')

        if not all([id_cliente, id_lote, valor_venda]):
            messages.error(request, 'Preencha todos os campos obrigatórios.', extra_tags='danger')
            return redirect('vendas:cadastrar_venda')

        lote = get_object_or_404(Lote, id=id_lote, empresa=request.user.empresa, status='D')
        cliente = get_object_or_404(Cliente, id=id_cliente, empresa=request.user.empresa)

        venda = Vendas.objects.create(
            id_lote=lote,
            id_cliente=cliente,
            valor_venda=valor_venda,
            empresa=request.user.empresa,
        )

        lote.status = 'V'
        lote.proprietario = cliente
        lote.save()

        if valor_entrada and float(valor_entrada) > 0:
            Pagamento.objects.create(
                id_venda=venda,
                forma_pagamento=forma_pagamento,
                valor=valor_entrada,
                empresa=request.user.empresa,
            )

        messages.success(request, 'Venda cadastrada com sucesso!')
        return redirect('vendas:detalhe_venda', pk=venda.id_venda)


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_vendas)
def detalhe_venda(request, pk):
    venda = get_object_or_404(Vendas, id_venda=pk, empresa=request.user.empresa)
    pagamentos = venda.pagamento_set.all()
    return render(request, 'vendas/detalhe_venda.html', {
        'venda': venda,
        'pagamentos': pagamentos,
    })


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_vendas)
def registrar_pagamento(request, pk):
    venda = get_object_or_404(Vendas, id_venda=pk, empresa=request.user.empresa)

    if venda.status_venda == 'Cancelada':
        messages.error(request, 'Não é possível registrar pagamento em venda cancelada.', extra_tags='danger')
        return redirect('vendas:detalhe_venda', pk=pk)

    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        valor = request.POST.get('valor')
        observacao = request.POST.get('observacao', '')

        if not all([forma_pagamento, valor]):
            messages.error(request, 'Preencha todos os campos.', extra_tags='danger')
            return redirect('vendas:detalhe_venda', pk=pk)

        with transaction.atomic():
            Pagamento.objects.create(
                id_venda=venda,
                forma_pagamento=forma_pagamento,
                valor=valor,
                observacao=observacao,
                empresa=request.user.empresa,
            )

            if venda.saldo_restante() <= 0:
                venda.quitado = True
                venda.status_venda = 'Concluída'
                venda.save()

        messages.success(request, 'Pagamento registrado com sucesso!')
    return redirect('vendas:detalhe_venda', pk=pk)


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_vendas)
def cancelar_venda(request, pk):
    venda = get_object_or_404(Vendas, id_venda=pk, empresa=request.user.empresa)

    if venda.status_venda == 'Cancelada':
        messages.error(request, 'Venda já está cancelada.', extra_tags='danger')
        return redirect('vendas:detalhe_venda', pk=pk)

    with transaction.atomic():
        lote = venda.id_lote
        lote.status = 'D'
        lote.proprietario = None
        lote.save()

        venda.status_venda = 'Cancelada'
        venda.save()

    messages.success(request, 'Venda cancelada e lote liberado com sucesso!')
    return redirect('vendas:home_vendas')
