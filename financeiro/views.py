from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import ContaPagar, ContaReceber, Cheque, Fornecedor, DespesasCategoria
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator




@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def despesas(request):
    despesas = ContaPagar.objects.all()
    return render(request, 'despesas.html', {'despesas': despesas})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_despesas(request):
    if request.method == "GET":
        cadastrar_categorias = DespesasCategoria.objects.all()
        return render(request, 'cadastrar_despesas.html', {'categorias': cadastrar_categorias})
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        data_pagamento = request.POST.get('data_pagamento')
        forma_pagamento = request.POST.get('forma_pagamento')
        categoria = request.POST.get('categoria')
        pago = request.POST.get('pago')
        if pago == 'S':
            pago = True
        else:
            pago = False
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # Aqui você deve salvar os dados da conta a pagar no banco de dados
        despesas = ContaPagar(descricao=descricao, valor=valor, data_vencimento=data_vencimento, data_pagamento=data_pagamento, forma_pagamento=forma_pagamento, categoria=DespesasCategoria.objects.get(id=categoria), pago=pago)
        despesas.save()
        return redirect('/financeiro/despesas/')
    


    
@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def editar_despesas(request, id):
    despesas = ContaPagar.objects.get(id=id)
    categorias = DespesasCategoria.objects.all()
    if request.method == "GET":
        return render(request, 'cadastrar_despesas.html', {'despesas': despesas, 'categorias': categorias})
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        forma_pagamento = request.POST.get('forma_pagamento')
        pago = request.POST.get('pago')
        categoria = request.POST.get('categoria')
        print(pago)
        if pago == 'S':
            pago = True
        else:
            pago = False
        print("aqui é a categoria: "+categoria +" e aqui é se ta pago: "+str(pago))
        # Aqui você deve atualizar os dados da conta a pagar no banco de dados
        despesas.descricao = descricao
        despesas.valor = valor
        despesas.data_vencimento = data_vencimento
        despesas.forma_pagamento = forma_pagamento
        despesas.pago = pago
        despesas.categoria = DespesasCategoria.objects.get(id=categoria)
        despesas.save()
        return redirect('/financeiro/despesas/')
    
@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def excluir_despesas(request, id):
    despesas = ContaPagar.objects.get(id=id)
    despesas.delete()
    return redirect('/financeiro/despesas/')


@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def total_despesas(request):
    despesas = ContaPagar.objects.all()
    total_valor = 0
    total_despesas = {
        'D': 0,
        'C': 0,
        'B': 0,
        'T': 0,
        'P': 0,
    
    }
    for despesa in despesas:
        total_valor += despesa.valor
        total_despesas[despesa.forma_pagamento] += despesa.valor

    total_despesas['Dinheiro'] = total_despesas.pop('D')
    total_despesas['Cartão de Crédito'] = total_despesas.pop('C')
    total_despesas['Boleto'] = total_despesas.pop('B')
    total_despesas['Transferência Bancária'] = total_despesas.pop('T')
    total_despesas['PIX'] = total_despesas.pop('P')


    return JsonResponse({'total_valor': total_valor, 'total_despesas': total_despesas})


#categoria

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_categorias(request):
    if request.method == "GET":
        cadastrar_categorias = DespesasCategoria.objects.all()
        return render(request, 'cadastrar_categoria.html', {'categorias': cadastrar_categorias})
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        print(descricao)
        # Aqui você deve salvar os dados da categoria no banco de dados
        categoria = DespesasCategoria(descricao=descricao)
        categoria.save()
        return redirect('/financeiro/despesas/')


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
        return redirect('contas_receber')
    
@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
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
@has_role_decorator("vendedor")
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
@has_role_decorator("vendedor")
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
        return redirect('cheques')
    

@login_required(login_url='/auth/login/')
def excluir_cheque(request, id):
    cheque = Cheque.objects.get(id=id)
    cheque.delete()
    return redirect('cheques')




# Path: imperio/financeiro/models.py
@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'fornecedores.html', {'fornecedores': fornecedores})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_fornecedor(request):
    if request.method == "GET":
        return render(request, 'cadastrar_fornecedor.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        print(nome, cnpj)
        # Aqui você deve salvar os dados do fornecedor no banco de dados
        fornecedor = Fornecedor(nome=nome, cnpj=cnpj)
        fornecedor.save()
        return redirect('fornecedores')
    

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def editar_fornecedor(request, id):
    fornecedor = Fornecedor.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'editar_fornecedor.html', {'fornecedor': fornecedor})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        print(nome, cnpj)
        # Aqui você deve atualizar os dados do fornecedor no banco de dados
        fornecedor.nome = nome
        fornecedor.cnpj = cnpj
        fornecedor.save()
        return redirect('fornecedores')
    

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def excluir_fornecedor(request, id):
    fornecedor = Fornecedor.objects.get(id=id)
    fornecedor.delete()
    return redirect('fornecedores')



    