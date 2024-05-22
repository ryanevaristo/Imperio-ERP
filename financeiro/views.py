from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from cliente.models import Cliente
from .models import ContaPagar, ContaReceber, Cheque, Fornecedor, DespesasCategoria
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
import pandas as pd
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
import tempfile
import io



@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def despesas(request):
    despesas = ContaPagar.objects.all()
    paginator = Paginator(despesas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj = page_obj[::-1]

    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        despesas = ContaPagar.objects.filter(data_vencimento__range=[start_date, end_date])
        paginator = Paginator(despesas, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    if request.GET.get('pesquisar'):
        pesquisar = request.GET.get('pesquisar')
        despesas = ContaPagar.objects.filter(descricao__icontains=pesquisar)
        paginator = Paginator(despesas, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'despesas.html', {'page_obj': page_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_despesas(request):
    if request.method == "GET":
        cadastrar_categorias = DespesasCategoria.objects.all()
        return render(request, 'cadastrar_despesas.html', {'categorias': cadastrar_categorias})
    elif request.method == "POST" and request.POST.get('descricao_categoria') =='':
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
        print(request.POST)
    else:
        descricao_categoria = request.POST.get('descricao_categoria')
        if DespesasCategoria.objects.filter(nome_categoria=descricao_categoria).exists():
            messages.error(request,'Categoria já cadastrada', extra_tags='danger')
            return redirect("financeiro:cadastrar_despesas")
        
        categorias = DespesasCategoria(nome_categoria=descricao_categoria)
        categorias.save()
        print(request.path_info)
        return HttpResponseRedirect(request.path_info)
        
    print(request.POST)

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
        data_pagamento = request.POST.get('data_pagamento')
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
        despesas.data_pagamento = data_pagamento
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
def total_despesas_m_atual(request):
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

def total_despesas(request):
    despesas = ContaPagar.objects.all()
    total_valor = 0
    for despesa in despesas:
        total_valor += despesa.valor
    return JsonResponse({'total_valor': total_valor})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def exportar_despesas_xlsx(request):
    despesas = ContaPagar.objects.all()
    
    df = pd.DataFrame(list(despesas.values()))
    df['categoria'] = df['categoria_id'].apply(lambda x: DespesasCategoria.objects.get(id=x).descricao)
    df.drop('categoria_id', axis=1, inplace=True)

    df['forma_pagamento'] = df['forma_pagamento'].apply(lambda x: dict(ContaPagar.choice_forma_pagamento)[x])
    output = io.BytesIO()
    excel = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(excel, sheet_name='Sheet1', index=False)
    excel.close()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=despesas.xlsx'
    return response

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def exportar_despesas_pdf(request):
    despesas = ContaPagar.objects.all()
    df = pd.DataFrame(list(despesas.values()))
    df['categoria'] = df['categoria_id'].apply(lambda x: DespesasCategoria.objects.get(id=x).descricao)
    df.drop('categoria_id', axis=1, inplace=True)
    output = io.BytesIO()
    excel = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(excel, sheet_name='Sheet1', index=False)
    excel.close()
    output.seek(0)
    response = HttpResponse(output, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=despesas.pdf'
    return response

    

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
    entrada = ContaReceber.objects.filter(recebido=True)
    paginator = Paginator(entrada, 10)
    page_number = request.GET.get('page')
    entrada_obj = paginator.get_page(page_number)

    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        entrada_obj = ContaReceber.objects.filter(data_vencimento__range=[start_date, end_date])
        paginator = Paginator(entrada_obj, 10)
        page_number = request.GET.get('page')
        entrada_obj = paginator.get_page(page_number)
    
    if request.GET.get('pesquisar'):
        pesquisar = request.GET.get('pesquisar')
        entrada_obj = ContaReceber.objects.filter(descricao__icontains=pesquisar)
        paginator = Paginator(entrada_obj, 10)
        page_number = request.GET.get('page')
        entrada_obj = paginator.get_page(page_number)

    return render(request, 'entradas.html', {'entrada_obj': entrada_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def contas_a_receber(request):
    entrada = ContaReceber.objects.filter(recebido=False)
    paginator = Paginator(entrada, 10)
    page_number = request.GET.get('page')
    entrada_obj = paginator.get_page(page_number)

    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        entrada_obj = ContaReceber.objects.filter(data_vencimento__range=[start_date, end_date])
        paginator = Paginator(entrada_obj, 10)
        page_number = request.GET.get('page')
        entrada_obj = paginator.get_page(page_number)
    
    if request.GET.get('pesquisar'):
        pesquisar = request.GET.get('pesquisar')
        entrada_obj = ContaReceber.objects.filter(descricao__icontains=pesquisar)
        paginator = Paginator(entrada_obj, 10)
        page_number = request.GET.get('page')
        entrada_obj = paginator.get_page(page_number)

    return render(request, 'contas_receber.html', {'entrada_obj': entrada_obj})

@login_required(login_url='/auth/login/')
def cadastrar_entrada(request):
    if request.method == "GET":
        clientes = Cliente.objects.all()
        return render(request, 'cadastrar_entrada.html', {'clientes': clientes})
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
        cliente = int(cliente)
        # Aqui você deve salvar os dados da conta a receber no banco de dados
        conta_receber = ContaReceber(cliente=Cliente.objects.get(id=cliente),descricao=descricao, valor=valor, data_vencimento=data_vencimento, data_recebimento=data_recebimento, forma_recebimento=forma_recebimento, recebido=recebido)
        conta_receber.save()
        messages.success(request, "Entrada Cadastrada com Sucesso!")
        return redirect('financeiro:entradas')
    
@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def editar_entrada(request, id):
    entrada = ContaReceber.objects.get(id=id)
    clientes = Cliente.objects.all()
    if request.method == "GET":
        return render(request, 'cadastrar_entrada.html', {'entrada': entrada, 'clientes': clientes})
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
        entrada.cliente = Cliente.objects.get(id=cliente)
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
def total_entradas(request):
    entradas = ContaReceber.objects.all()
    total_valor = 0
    for entrada in entradas:
        total_valor += entrada.valor
    return JsonResponse({'total_valor': total_valor})



@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def exportar_entrada_xlsx(request):
    entrada = ContaReceber.objects.all()
    
    df = pd.DataFrame(list(entrada.values()))
    df['forma_recebimento'] = df['forma_recebimento'].apply(lambda x: dict(ContaReceber.choice_forma_recebimento)[x])
    output = io.BytesIO()
    excel = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(excel, sheet_name='Sheet1', index=False)
    excel.close()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=entrada.xlsx'
    return response

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cheques(request):
    cheques = Cheque.objects.all()
    paginator = Paginator(cheques, 10)
    page_number = request.GET.get('page')
    cheques_obj = paginator.get_page(page_number)

    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        cheques_obj = Cheque.objects.filter(data_compensacao__range=[start_date, end_date])
        paginator = Paginator(cheques_obj, 10)
        page_number = request.GET.get('page')
        cheques_obj = paginator.get_page(page_number)


    if request.GET.get('pesquisar'):
        pesquisar = request.GET.get('pesquisar')
        cheques_obj = Cheque.objects.filter(nome_titular__icontains=pesquisar)
        paginator = Paginator(cheques_obj, 10)
        page_number = request.GET.get('page')
        
        
    return render(request, 'cheques/cheques.html', {'cheques_obj': cheques_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_cheque(request):
    if request.method == "GET":
        clientes = Cliente.objects.all()
        return render(request, 'cheques/cadastrar_cheque.html', {'clientes': clientes})
    elif request.method == "POST":
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        data_compensacao = request.POST.get('data_compensacao')
        nome_titular = request.POST.get('cliente')
        nome_repassador = request.POST.get('nome_repassador')
        banco = request.POST.get('banco')
        status = request.POST.get('status')
        cheque_unico = Cheque.objects.filter(numero=numero)
        if cheque_unico.exists():
            messages.error(request,'Cheque já cadastrado', extra_tags='danger')
            return redirect("financeiro:cadastrar_cheque")
        cheque = Cheque(numero=numero, valor=valor,  data_compensacao=data_compensacao, nome_titular=Cliente.objects.get(id=nome_titular), banco=banco, nome_repassador=nome_repassador, situacao=status)
        cheque.save()
        return redirect('financeiro:cheques')


@login_required(login_url='/auth/login/')
def editar_cheque(request, id):
    cheque = Cheque.objects.get(id=id)
    if request.method == "GET":
        clientes = Cliente.objects.all()
        return render(request, 'cheques/cadastrar_cheque.html', {'cheque': cheque, 'clientes': clientes})
    elif request.method == "POST":
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        data_compensacao = request.POST.get('data_compensacao')
        nome_titular = request.POST.get('cliente')
        nome_repassador = request.POST.get('nome_repassador')
        status = request.POST.get('status')
        banco = request.POST.get('banco')

        # Aqui você deve atualizar os dados do cheque no banco de dados
        cheque.numero = numero
        cheque.valor = valor
        cheque.data_compensacao = data_compensacao
        cheque.nome_titular = Cliente.objects.get(id=nome_titular)
        cheque.banco = banco
        cheque.nome_repassador = nome_repassador
        cheque.situacao = status
        cheque.save()
        return redirect('financeiro:cheques')
    

@login_required(login_url='/auth/login/')
def excluir_cheque(request, id):
    cheque = Cheque.objects.get(id=id)
    cheque.delete()
    return redirect('financeiro:cheques')



@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def exportar_cheque_xlsx(request):
    cheques = Cheque.objects.all()
    
    df = pd.DataFrame(list(cheques.values()))
    df['situacao'] = df['situacao'].apply(lambda x: dict(Cheque.choice_situacao)[x])
    df['banco'] = df['banco'].apply(lambda x: dict(Cheque.choice_banco)[x])
    output = io.BytesIO()
    excel = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(excel, sheet_name='Sheet1', index=False)
    excel.close()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=cheques.xlsx'
    return response




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



@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def caixa(request):
    cheques = Cheque.objects.all()
    total_valor = 0
    total_valor_compensado = 0
    total_valor_repassado = 0
    for cheque in cheques:
        total_valor += cheque.valor
        if cheque.situacao == 'C':
                total_valor_compensado += cheque.valor
        elif cheque.situacao == 'R':
            total_valor_repassado += cheque.valor

    entradas = ContaReceber.objects.filter(recebido=True)
    total_entradas = 0
    for entrada in entradas:
        total_entradas += entrada.valor
    
    despesas = ContaPagar.objects.all()
    total_despesas = 0
    for despesa in despesas:
        total_despesas += despesa.valor

    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        despesas = ContaPagar.objects.filter(data_vencimento__range=[start_date, end_date])
        total_despesas = 0
        for despesa in despesas:
            total_despesas += despesa.valor
        
        entradas = ContaReceber.objects.filter(data_vencimento__range=[start_date, end_date], recebido=True)
        total_entradas = 0
        for entrada in entradas:
            total_entradas += entrada.valor
        
        cheque = Cheque.objects.filter(data_compensacao__range=[start_date, end_date])
        total_valor_repassado = 0
        total_valor_compensado = 0

        for cheque in cheques:
            if cheque.situacao == 'C':
                total_valor_compensado += cheque.valor
            elif cheque.situacao == 'R':
                total_valor_repassado += cheque.valor
        
        return render(request, 'caixa.html', {'saldo': (total_entradas) - total_despesas, 'total_entradas': total_entradas, 'total_despesas': total_despesas, 'total_cheques': total_valor, 'total_valor_repassado': total_valor_repassado, 'total_valor_compensado': total_valor_compensado})
    return render(request, 'caixa.html', {'saldo': (total_entradas) - total_despesas , 'total_entradas': total_entradas, 'total_despesas': total_despesas, 'total_cheques': total_valor, 'total_valor_repassado': total_valor_repassado, 'total_valor_compensado': total_valor_compensado})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def saldo_anual(request):
    meses_anteriores = [1,2,3,4,5,6,7,8,9,10,11,12]
    saldo = []
    for mes in meses_anteriores:
        despesas = ContaPagar.objects.filter(data_vencimento__month=mes)
        total_despesas = 0
        for despesa in despesas:
            total_despesas += despesa.valor
        
        entradas = ContaReceber.objects.filter(data_vencimento__month=mes)
        total_entradas = 0
        for entrada in entradas:
            total_entradas += entrada.valor
        
        saldo.append(total_entradas - total_despesas)
    return JsonResponse({'saldo': saldo, 'meses': meses_anteriores})