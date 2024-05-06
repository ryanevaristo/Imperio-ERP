from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import ContaPagar, ContaReceber, Cheque, Fornecedor, DespesasCategoria
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
import pandas as pd
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime



@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def despesas(request):
    despesas = ContaPagar.objects.all()
    paginator = Paginator(despesas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj = page_obj[::-1]

    return render(request, 'despesas.html', {'page_obj': page_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_despesas(request):
    if request.method == "GET":
        cadastrar_categorias = DespesasCategoria.objects.all()
        return render(request, 'cadastrar_despesas.html', {'categorias': cadastrar_categorias})
    elif request.method == "POST" and "descricao_categoria" not in request.POST:
        print(request.POST)
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
        
        # Aqui você deve salvar os dados da conta a pagar no banco de dados
        despesas = ContaPagar(descricao=descricao, valor=valor, data_vencimento=data_vencimento, data_pagamento=data_pagamento, forma_pagamento=forma_pagamento, categoria=DespesasCategoria.objects.get(id=categoria), pago=pago)
        despesas.save()
    else:
        descricao_categoria = request.POST.get('descricao_categoria')
        categorias = DespesasCategoria(descricao=descricao_categoria)
        categorias.save()
        return  HttpResponseRedirect(request.path_info)

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
    #maiores despesas no mês atual
    # despesas = ContaPagar.objects.filter(data_vencimento__month=9)
    despesas = ContaPagar.objects.filter(data_vencimento__month=datetime.now().month).order_by('-valor')[:5]
    total_valor = 0
    total_despesas = {

    
    }
    for despesa in despesas:
        total_valor += despesa.valor
        total_despesas[despesa.descricao] = despesa.valor



    return JsonResponse({'total_valor': total_valor, 'total_despesas': total_despesas, 'mes_atual': datetime.now().month})


@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def gerar_excel_despesas(request):
    despesas = ContaPagar.objects.all()
    
    df = pd.DataFrame(columns=['Descrição', 'Valor', 'Data de Vencimento', 'Data de Pagamento', 'Forma de Pagamento', 'Categoria', 'Pago'])
    for despesa in despesas:
        df = df.append({'Descrição': despesa.descricao, 'Valor': despesa.valor, 'Data de Vencimento': despesa.data_vencimento, 'Data de Pagamento': despesa.data_pagamento, 'Forma de Pagamento': despesa.forma_pagamento, 'Categoria': despesa.categoria, 'Pago': despesa.pago}, ignore_index=True)

    df.to_excel('despesas.xlsx', index=False)
    return HttpResponse("Excel gerado com sucesso!")


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
def entrada(request):
    entrada = ContaReceber.objects.all()
    paginator = Paginator(entrada, 10)
    page_number = request.GET.get('page')
    entrada_obj = paginator.get_page(page_number)
    return render(request, 'entradas.html', {'entrada_obj': entrada_obj})

@login_required(login_url='/auth/login/')
def cadastrar_entrada(request):
    if request.method == "GET":
        return render(request, 'cadastrar_entrada.html')
    elif request.method == "POST":
        cliente = request.POST.get('cliente')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        data_recebimento = request.POST.get('data_recebimento')
        forma_recebimento = request.POST.get('forma_recebimento')
        recebido = request.POST.get('recebido')
        if recebido == 'S':
            recebido = True
        else:
            recebido = False
        print(descricao, valor, data_vencimento, forma_recebimento, recebido)
        # Aqui você deve salvar os dados da conta a receber no banco de dados
        conta_receber = ContaReceber(cliente=cliente,descricao=descricao, valor=valor, data_vencimento=data_vencimento, data_recebimento=data_recebimento, forma_recebimento=forma_recebimento, recebido=recebido)
        conta_receber.save()
        return redirect('financeiro:entradas')
    
@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def editar_entrada(request, id):
    entrada = ContaReceber.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'cadastrar_entrada.html', {'entrada': entrada})
    elif request.method == "POST":
        cliente = request.POST.get('cliente')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_vencimento = request.POST.get('data_vencimento')
        data_recebimento = request.POST.get('data_recebimento')
        forma_recebimento = request.POST.get('forma_recebimento')
        recebido = request.POST.get('recebido')
        if recebido == 'S':
            recebido = True
        else:
            recebido = False
        print(descricao, valor, data_vencimento, forma_recebimento, recebido)
        # Aqui você deve atualizar os dados da conta a receber no banco de dados
        entrada.cliente = cliente
        entrada.descricao = descricao
        entrada.valor = valor
        entrada.data_vencimento = data_vencimento
        entrada.data_recebimento = data_recebimento
        entrada.forma_recebimento = forma_recebimento
        entrada.recebido = recebido
        entrada.save()
        return redirect('financeiro:entradas')
    

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def excluir_entrada(request, id):
    conta_receber = ContaReceber.objects.get(id=id)
    conta_receber.delete()
    return redirect('financeiro:entradas')


@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cheques(request):
    cheques = Cheque.objects.all()
    paginator = Paginator(cheques, 10)
    page_number = request.GET.get('page')
    cheques_obj = paginator.get_page(page_number)
    return render(request, 'cheques/cheques.html', {'cheques_obj': cheques_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_cheque(request):
    if request.method == "GET":
        return render(request, 'cheques/cadastrar_cheque.html')
    elif request.method == "POST":
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        data_compensacao = request.POST.get('data_compensacao')
        nome_titular = request.POST.get('nome_titular')
        nome_repassador = request.POST.get('nome_repassador')
        banco = request.POST.get('banco')
        print(numero, valor, data_compensacao, nome_titular, banco)
        # Aqui você deve salvar os dados do cheque no banco de dados
        cheque_unico = Cheque.objects.filter(numero=numero)
        if cheque_unico.exists():
            messages.error(request,'Cheque já cadastrado', extra_tags='danger')
            return redirect("financeiro:cadastrar_cheque")
        cheque = Cheque(numero=numero, valor=valor,  data_compensacao=data_compensacao, nome_titular=nome_titular, banco=banco, nome_repassador=nome_repassador)
        cheque.save()
        return redirect('financeiro:cheques')


@login_required(login_url='/auth/login/')
def editar_cheque(request, id):
    cheque = Cheque.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'cheques/cadastrar_cheque.html', {'cheque': cheque})
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
        return redirect('financeiro:cheques')
    

@login_required(login_url='/auth/login/')
def excluir_cheque(request, id):
    cheque = Cheque.objects.get(id=id)
    cheque.delete()
    return redirect('financeiro:cheques')




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



    