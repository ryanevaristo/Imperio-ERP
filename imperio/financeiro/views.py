from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import ContaPagar, ContaReceber, Cheque
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator


@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def contas_pagar(request):
    contas_pagar = ContaPagar.objects.all()
    return render(request, 'contas_pagar.html', {'contas_pagar': contas_pagar})

@login_required(login_url='/auth/login/')
def cadastrar_contas_pagar(request):
    if request.method == "GET":
        return render(request, 'cadastrar_contas_pagar.html')
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        forma_pagamento = request.POST.get('forma_pagamento')
        pago = request.POST.get('pago')
        print(descricao, valor, data_vencimento, forma_pagamento, pago)
        # Aqui você deve salvar os dados da conta a pagar no banco de dados
        conta_pagar = ContaPagar(descricao=descricao, valor=valor, data_vencimento=data_vencimento, forma_pagamento=forma_pagamento, pago=pago)
        conta_pagar.save()
        return HttpResponse("Conta a pagar cadastrada com sucesso!")
    
@login_required(login_url='/auth/login/')
def editar_contas_pagar(request, id):
    conta_pagar = ContaPagar.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'editar_contas_pagar.html', {'conta_pagar': conta_pagar})
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        forma_pagamento = request.POST.get('forma_pagamento')
        pago = request.POST.get('pago')
        print(descricao, valor, data_vencimento, forma_pagamento, pago)
        # Aqui você deve atualizar os dados da conta a pagar no banco de dados
        conta_pagar.descricao = descricao
        conta_pagar.valor = valor
        conta_pagar.data_vencimento = data_vencimento
        conta_pagar.forma_pagamento = forma_pagamento
        conta_pagar.pago = pago
        conta_pagar.save()
        return HttpResponse("Conta a pagar atualizada com sucesso!")
    
@login_required(login_url='/auth/login/')
def excluir_contas_pagar(request, id):
    conta_pagar = ContaPagar.objects.get(id=id)
    conta_pagar.delete()
    return HttpResponse("Conta a pagar excluída com sucesso!")

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def contas_receber(request):
    contas_receber = ContaReceber.objects.all()
    return render(request, 'contas_receber.html', {'contas_receber': contas_receber})

@login_required(login_url='/auth/login/')
def cadastrar_contas_receber(request):
    if request.method == "GET":
        return render(request, 'cadastrar_contas_receber.html')
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        forma_recebimento = request.POST.get('forma_recebimento')
        recebido = request.POST.get('recebido')
        print(descricao, valor, data_vencimento, forma_recebimento, recebido)
        # Aqui você deve salvar os dados da conta a receber no banco de dados
        conta_receber = ContaReceber(descricao=descricao, valor=valor, data_vencimento=data_vencimento, forma_recebimento=forma_recebimento, recebido=recebido)
        conta_receber.save()
        return HttpResponse("Conta a receber cadastrada com sucesso!")
    
@login_required(login_url='/auth/login/')
def editar_contas_receber(request, id):
    conta_receber = ContaReceber.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'editar_contas_receber.html', {'conta_receber': conta_receber})
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        forma_recebimento = request.POST.get('forma_recebimento')
        recebido = request.POST.get('recebido')
        print(descricao, valor, data_vencimento, forma_recebimento, recebido)
        # Aqui você deve atualizar os dados da conta a receber no banco de dados
        conta_receber.descricao = descricao
        conta_receber.valor = valor
        conta_receber.data_vencimento = data_vencimento
        conta_receber.forma_recebimento = forma_recebimento
        conta_receber.recebido = recebido
        conta_receber.save()
        return HttpResponse("Conta a receber atualizada com sucesso!")
    

@login_required(login_url='/auth/login/')
def excluir_contas_receber(request, id):
    conta_receber = ContaReceber.objects.get(id=id)
    conta_receber.delete()
    return HttpResponse("Conta a receber excluída com sucesso!")


@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cheques(request):
    cheques = Cheque.objects.all()
    return render(request, 'cheques.html', {'cheques': cheques})

@login_required(login_url='/auth/login/')
def cadastrar_cheque(request):
    if request.method == "GET":
        return render(request, 'cadastrar_cheque.html')
    elif request.method == "POST":
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        data_compensacao = request.POST.get('data_compensacao')
        emitente = request.POST.get('emitente')
        print(numero, valor, data_vencimento, data_compensacao, emitente)
        # Aqui você deve salvar os dados do cheque no banco de dados
        cheque = Cheque(numero=numero, valor=valor, data_vencimento=data_vencimento, data_compensacao=data_compensacao, emitente=emitente)
        cheque.save()
        return HttpResponse("Cheque cadastrado com sucesso!")


@login_required(login_url='/auth/login/')
def editar_cheque(request, id):
    cheque = Cheque.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'editar_cheque.html', {'cheque': cheque})
    elif request.method == "POST":
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        data_compensacao = request.POST.get('data_compensacao')
        emitente = request.POST.get('emitente')
        print(numero, valor, data_vencimento, data_compensacao, emitente)
        # Aqui você deve atualizar os dados do cheque no banco de dados
        cheque.numero = numero
        cheque.valor = valor
        cheque.data_vencimento = data_vencimento
        cheque.data_compensacao = data_compensacao
        cheque.emitente = emitente
        cheque.save()
        return HttpResponse("Cheque atualizado com sucesso!")
    

@login_required(login_url='/auth/login/')
def excluir_cheque(request, id):
    cheque = Cheque.objects.get(id=id)
    cheque.delete()
    return HttpResponse("Cheque excluído com sucesso!")

# Path: imperio/financeiro/models.py