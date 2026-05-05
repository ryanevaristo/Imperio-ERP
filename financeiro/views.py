from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from cliente.models import Cliente
from .models import ContaPagar, ContaReceber, Cheque, Fornecedor, DespesasCategoria
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
import pandas as pd
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime

from global_variables import lista_permissoes_financeiro

import io



@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def despesas(request):
   # Obtém todas as despesas
    despesas = ContaPagar.objects.filter(empresa=request.user.empresa)

    # Filtra por data, se os parâmetros estiverem presentes
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        despesas = despesas.filter(data_pagamento__range=[start_date, end_date])

    # Filtra por pesquisa, se o parâmetro estiver presente
    pesquisar = request.GET.get('pesquisar')
    if pesquisar:
        despesas = despesas.filter(descricao__icontains=pesquisar)

    # Cria o paginador
    paginator = Paginator(despesas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if start_date and end_date is None:
        return render(request, 'despesas.html', {'page_obj': page_obj, 'pesquisar': pesquisar})
        
    

    return render(request, 'despesas.html', {'page_obj': page_obj, 'start_date': start_date, 'end_date': end_date, 'pesquisar': pesquisar})

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def cadastrar_despesas(request):
    if request.method == "GET":
        cadastrar_categorias = DespesasCategoria.objects.all()
        return render(request, 'cadastrar_despesas.html', {'categorias': cadastrar_categorias})
    elif request.method == "POST" and request.POST.get('descricao_categoria') =='':
        print(request.POST)
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_pagamento = request.POST.get('data_pagamento')
        forma_pagamento = request.POST.get('forma_pagamento')
        categoria = request.POST.get('categoria')
        pago = request.POST.get('pago')
        if pago == 'S':
            pago = True
        else:
            pago = False

        if data_pagamento == '': 
            data_pagamento = '1900-01-01'
        # Aqui você deve salvar os dados da conta a pagar no banco de dados
        despesas = ContaPagar(descricao=descricao, valor=valor,
                               data_pagamento=data_pagamento,
                               forma_pagamento=forma_pagamento,
                               categoria=DespesasCategoria.objects.get(id=categoria),
                               pago=pago, empresa=request.user.empresa)
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
@has_role_decorator(lista_permissoes_financeiro)
def editar_despesas(request, id):
    despesas = get_object_or_404(ContaPagar, id=id, empresa=request.user.empresa)
    categorias = DespesasCategoria.objects.all()
    if request.method == "GET":
        return render(request, 'cadastrar_despesas.html', {'despesas': despesas, 'categorias': categorias})
    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
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
        despesas.data_pagamento = data_pagamento
        despesas.forma_pagamento = forma_pagamento
        despesas.pago = pago
        despesas.categoria = DespesasCategoria.objects.get(id=categoria)
        despesas.save()
        return redirect('/financeiro/despesas/')
    
@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def excluir_despesas(request, id):
    despesas = get_object_or_404(ContaPagar, id=id, empresa=request.user.empresa)
    despesas.delete()
    return redirect('/financeiro/despesas/')


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def total_despesas_m_atual(request):
    despesas = ContaPagar.objects.filter(empresa=request.user.empresa)
    #maiores despesas no mês atual
    despesas = ContaPagar.objects.filter(data_pagamento__month=datetime.now().month, empresa=request.user.empresa).order_by('-valor')[:5]
    total_valor = 0
    total_despesas = {

    
    }
    for despesa in despesas:
        total_valor += despesa.valor
        total_despesas[despesa.descricao] = despesa.valor



    return JsonResponse({'total_valor': total_valor, 'total_despesas': total_despesas, 'mes_atual': datetime.now().month})

def total_despesas(request):
    despesas = ContaPagar.objects.filter(empresa=request.user.empresa)
    total_valor = 0
    for despesa in despesas:
        total_valor += despesa.valor
    return JsonResponse({'total_valor': total_valor})

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def exportar_despesas_xlsx(request):
    # Otimizado: Usa select_related para categoria e only() para campos necessários
    despesas = ContaPagar.objects.select_related('categoria').filter(
        empresa=request.user.empresa
    ).only(
        'descricao', 'valor', 'data_pagamento', 'forma_pagamento', 
        'pago', 'categoria__nome_categoria'
    ).order_by('-data_pagamento')
    
    # Cria lista de dicionários diretamente sem queries adicionais
    despesas_data = []
    for despesa in despesas:
        despesas_data.append({
            'Descrição': despesa.descricao,
            'Valor': float(despesa.valor),
            'Data Pagamento': despesa.data_pagamento.strftime('%d/%m/%Y') if despesa.data_pagamento else '',
            'Forma Pagamento': dict(ContaPagar.choice_forma_pagamento).get(despesa.forma_pagamento, ''),
            'Pago': 'Sim' if despesa.pago else 'Não',
            'Categoria': despesa.categoria.nome_categoria if despesa.categoria else ''
        })
    
    df = pd.DataFrame(despesas_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as excel:
        df.to_excel(excel, sheet_name='Despesas', index=False)
    
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=despesas.xlsx'
    return response

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def importar_despesa_xlsx(request):
    if request.method == "POST":
        file = request.FILES['file']
        df = pd.read_excel(file, header=1,sheet_name='sheet2')
        df.columns = ['Data','Valor','Descrição','Forma']
        df = df.dropna(subset=["Data","Forma"])
        df['Valor'] = df["Valor"].fillna(0)
        categoria = DespesasCategoria.objects.get(id=1)
        choice_forma_recebimento = (
            ('DINHEIRO ', 'D'),
            ('DINHEIRO', 'D'),
            ('BANCO', 'T'),
        )
        df['Forma'] = df['Forma'].apply(lambda x: dict(choice_forma_recebimento)[x])
    
        for index, row in df.iterrows():
            conta_receber = ContaPagar(descricao=row['Descrição'], valor=row["Valor"], forma_pagamento=row["Forma"], data_pagamento=row["Data"],categoria=categoria,pago=True)
            conta_receber.save()

        return redirect('financeiro:despesas')

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def exportar_despesas_pdf(request):
    despesas = ContaPagar.objects.filter(empresa=request.user.empresa)
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
@has_role_decorator(lista_permissoes_financeiro)
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
@has_role_decorator(lista_permissoes_financeiro)
def entrada(request):
    entrada = ContaReceber.objects.filter(recebido=True, empresa=request.user.empresa)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        entrada = ContaReceber.objects.filter(data_recebimento__range=[start_date, end_date], empresa=request.user.empresa)

    pesquisar = request.GET.get('pesquisar')
    if pesquisar:
        entrada = ContaReceber.objects.filter(descricao__icontains=pesquisar, empresa=request.user.empresa)

    paginator = Paginator(entrada, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if start_date and end_date is None:
        return render(request, 'entradas.html', {'page_obj': page_obj, 'pesquisar': pesquisar})


    return render(request, 'entradas.html', {'page_obj': page_obj, 'start_date': start_date, 'end_date': end_date, 'pesquisar': pesquisar})

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def contas_a_receber(request):
    entrada = ContaReceber.objects.filter(recebido=False, empresa=request.user.empresa)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        entrada = ContaReceber.objects.filter(data_recebimento__range=[start_date, end_date], empresa=request.user.empresa)

    pesquisar = request.GET.get('pesquisar')
    if pesquisar:
        entrada = ContaReceber.objects.filter(descricao__icontains=pesquisar, empresa=request.user.empresa)
    
    paginator = Paginator(entrada, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if start_date and end_date is None:
        return render(request, 'contas_receber.html', {'entrada_obj': page_obj, 'pesquisar': pesquisar})
    
    return render(request, 'contas_receber.html', {'entrada_obj': page_obj, 'start_date': start_date, 'end_date': end_date, 'pesquisar': pesquisar})
@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def cadastrar_entrada(request):
    if request.method == "GET":
        clientes = Cliente.objects.filter(empresa=request.user.empresa)
        return render(request, 'cadastrar_entrada.html', {'clientes': clientes})
    elif request.method == "POST":
        cliente = request.POST.get('cliente')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_recebimento = request.POST.get('data_recebimento')
        forma_recebimento = request.POST.get('forma_recebimento')
        recebido = request.POST.get('recebido')
        if recebido == 'S':
            recebido = True
        else:
            recebido = False
        cliente = int(cliente)
        if data_recebimento == '': 
            messages.error(request,'Data de recebimento não pode ser vazia', extra_tags='danger')
            return redirect("financeiro:cadastrar_entrada")
        # Aqui você deve salvar os dados da conta a receber no banco de dados
        conta_receber = ContaReceber(cliente=Cliente.objects.get(id=cliente),descricao=descricao, valor=valor, data_recebimento=data_recebimento, forma_recebimento=forma_recebimento, recebido=recebido, empresa=request.user.empresa)
        conta_receber.save()
        messages.success(request, "Entrada Cadastrada com Sucesso!")
        return redirect('financeiro:entradas')
    

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def importar_entrada_xlsx(request):
    m = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    if request.method == "POST":
        file = request.FILES['file']
        try:
            df = pd.read_excel(file, header=2,sheet_name=f'ENTRADA {m[datetime.now().month].upper()} {datetime.now().year}')
        except:
            messages.error(request,'Planilha não encontrada', extra_tags='danger')
            return redirect("financeiro:contas_a_receber")
        

        df.columns = ['Data','Forma','Descrição','Valor']
        df = df.dropna(subset=["Data","Forma"])
        choice_forma_recebimento = (
            ('DINHEIRO', 'D'),
            ('BANCO', 'T'),
        )
        df['Forma'] = df['Forma'].apply(lambda x: dict(choice_forma_recebimento)[x])
    
        for index, row in df.iterrows():
            conta_receber = ContaReceber(cliente=Cliente.objects.get(id=2),descricao=row['Descrição'], valor=row["Valor"], data_recebimento=row["Data"],forma_recebimento=row["Forma"],recebido=True, empresa=request.user.empresa)
            conta_receber.save()

        

        return redirect('financeiro:entradas')
    
    
@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def editar_entrada(request, id):
    entrada = get_object_or_404(ContaReceber, id=id, empresa=request.user.empresa)
    clientes = Cliente.objects.filter(empresa=request.user.empresa)
    if request.method == "GET":
        return render(request, 'cadastrar_entrada.html', {'entrada': entrada, 'clientes': clientes})
    elif request.method == "POST":
        cliente = request.POST.get('cliente')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_recebimento = request.POST.get('data_recebimento')
        forma_recebimento = request.POST.get('forma_recebimento')
        recebido = request.POST.get('recebido')
        if recebido == 'S':
            recebido = True
        else:
            recebido = False
        # Aqui você deve atualizar os dados da conta a receber no banco de dados
        entrada.cliente = Cliente.objects.get(id=cliente)
        entrada.descricao = descricao
        entrada.valor = valor
        entrada.data_recebimento = data_recebimento
        entrada.forma_recebimento = forma_recebimento
        entrada.recebido = recebido
        entrada.save()
        return redirect('financeiro:entradas')
    

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def excluir_entrada(request, id):
    conta_receber = get_object_or_404(ContaReceber, id=id, empresa=request.user.empresa)
    conta_receber.delete()
    return redirect('financeiro:entradas')

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def total_entradas(request):
    entradas = ContaReceber.objects.filter(empresa=request.user.empresa)
    total_valor = 0
    for entrada in entradas:
        total_valor += entrada.valor
    return JsonResponse({'total_valor': total_valor})



@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def exportar_entrada_xlsx(request):
    # Otimizado: Usa select_related para cliente e only() para campos necessários
    entradas = ContaReceber.objects.select_related('cliente').filter(
        empresa=request.user.empresa
    ).only(
        'descricao', 'valor', 'data_recebimento', 'forma_recebimento',
        'recebido', 'cliente__nome_completo'
    ).order_by('-data_recebimento')
    
    # Cria lista de dicionários diretamente sem queries adicionais
    entradas_data = []
    for entrada in entradas:
        entradas_data.append({
            'Cliente': entrada.cliente.nome_completo if entrada.cliente else '',
            'Descrição': entrada.descricao,
            'Valor': float(entrada.valor),
            'Data Recebimento': entrada.data_recebimento.strftime('%d/%m/%Y') if entrada.data_recebimento else '',
            'Forma Recebimento': dict(ContaReceber.choice_forma_recebimento).get(entrada.forma_recebimento, ''),
            'Recebido': 'Sim' if entrada.recebido else 'Não'
        })
    
    df = pd.DataFrame(entradas_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as excel:
        df.to_excel(excel, sheet_name='Entradas', index=False)
    
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=entradas.xlsx'
    return response

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def cheques(request):
    cheques = Cheque.objects.filter(empresa=request.user.empresa)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        cheques = cheques.filter(data_compensacao__range=[start_date, end_date])

    pesquisar = request.GET.get('pesquisar')
    if pesquisar:
        cheques = cheques.filter(numero__icontains=pesquisar)

    paginator = Paginator(cheques, 10)
    page_number = request.GET.get('page')
    cheques_obj = paginator.get_page(page_number)
    if start_date and end_date is None:
        return render(request, 'cheques/cheques.html', {'cheques_obj': cheques_obj, 'pesquisar': pesquisar})
        
    return render(request, 'cheques/cheques.html', {'cheques_obj': cheques_obj, 'start_date': start_date, 'end_date': end_date, 'pesquisar': pesquisar})
        

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def cadastrar_cheque(request):
    if request.method == "GET":
        clientes = Cliente.objects.filter(empresa=request.user.empresa)
        return render(request, 'cheques/cadastrar_cheque.html', {'clientes': clientes})
    elif request.method == "POST":
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        data_compensacao = request.POST.get('data_compensacao')
        nome_titular = request.POST.get('cliente')
        nome_repassador = request.POST.get('nome_repassador')
        banco = request.POST.get('banco')
        status = request.POST.get('status')
        cheque_unico = Cheque.objects.filter(numero=numero, empresa=request.user.empresa)
        if cheque_unico.exists():
            messages.error(request,'Cheque já cadastrado', extra_tags='danger')
            return redirect("financeiro:cadastrar_cheque")
        titular = get_object_or_404(Cliente, id=nome_titular, empresa=request.user.empresa)
        cheque = Cheque(numero=numero, valor=valor, data_compensacao=data_compensacao, nome_titular=titular, banco=banco, nome_repassador=nome_repassador, situacao=status, empresa=request.user.empresa)
        cheque.save()
        return redirect('financeiro:cheques')


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def editar_cheque(request, id):
    cheque = get_object_or_404(Cheque, id=id, empresa=request.user.empresa)
    if request.method == "GET":
        clientes = Cliente.objects.filter(empresa=request.user.empresa)
        return render(request, 'cheques/cadastrar_cheque.html', {'cheque': cheque, 'clientes': clientes})
    elif request.method == "POST":
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        data_compensacao = request.POST.get('data_compensacao')
        nome_titular = request.POST.get('cliente')
        nome_repassador = request.POST.get('nome_repassador')
        status = request.POST.get('status')
        banco = request.POST.get('banco')

        cheque.numero = numero
        cheque.valor = valor
        cheque.data_compensacao = data_compensacao
        cheque.nome_titular = get_object_or_404(Cliente, id=nome_titular, empresa=request.user.empresa)
        cheque.banco = banco
        cheque.nome_repassador = nome_repassador
        cheque.situacao = status
        cheque.save()
        return redirect('financeiro:cheques')
    

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def excluir_cheque(request, id):
    cheque = get_object_or_404(Cheque, id=id, empresa=request.user.empresa)
    cheque.delete()
    return redirect('financeiro:cheques')



@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def exportar_cheque_xlsx(request):
    cheques = Cheque.objects.filter(empresa=request.user.empresa)
    
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
@has_role_decorator(lista_permissoes_financeiro)
def fornecedores(request):
    fornecedores = Fornecedor.objects.filter(empresa=request.user.empresa)
    return render(request, 'fornecedores.html', {'fornecedores': fornecedores})

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def cadastrar_fornecedor(request):
    if request.method == "GET":
        return render(request, 'cadastrar_fornecedor.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        print(nome, cnpj)
        # Aqui você deve salvar os dados do fornecedor no banco de dados
        fornecedor = Fornecedor(nome=nome, cnpj=cnpj, empresa=request.user.empresa)
        fornecedor.save()
        return redirect('fornecedores')
    

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id, empresa=request.user.empresa)
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
@has_role_decorator(lista_permissoes_financeiro)
def excluir_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id, empresa=request.user.empresa)
    fornecedor.delete()
    return redirect('fornecedores')



@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def caixa(request):
    from django.db.models import Sum, Case, When, Value, IntegerField

    empresa = request.user.empresa

    # Otimizado: Calcula totais usando agregações
    cheques_agg = Cheque.objects.filter(empresa=empresa).aggregate(
        total_cheques=Sum('valor'),
        total_compensado=Sum(Case(When(situacao='C', then='valor'), default=Value(0), output_field=IntegerField())),
        total_repassado=Sum(Case(When(situacao='R', then='valor'), default=Value(0), output_field=IntegerField())),
        total_emitido=Sum(Case(When(situacao='E', then='valor'), default=Value(0), output_field=IntegerField()))
    )

    entradas_agg = ContaReceber.objects.filter(
        recebido=True, empresa=empresa
    ).aggregate(total=Sum('valor'))

    despesas_agg = ContaPagar.objects.filter(
        pago=True, empresa=empresa
    ).aggregate(total=Sum('valor'))

    # Valores padrão se None
    total_cheques = float(cheques_agg['total_cheques'] or 0)
    total_compensado = float(cheques_agg['total_compensado'] or 0)
    total_repassado = float(cheques_agg['total_repassado'] or 0)
    total_emitido = float(cheques_agg['total_emitido'] or 0)
    total_entradas = float(entradas_agg['total'] or 0)
    total_despesas = float(despesas_agg['total'] or 0)

    # Filtro por data se fornecido
    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Recalcula para o período
        despesas_periodo = ContaPagar.objects.filter(
            data_pagamento__range=[start_date, end_date],
            pago=True,
            empresa=empresa
        ).aggregate(total=Sum('valor'))

        entradas_periodo = ContaReceber.objects.filter(
            data_recebimento__range=[start_date, end_date],
            recebido=True,
            empresa=empresa
        ).aggregate(total=Sum('valor'))

        total_despesas = float(despesas_periodo['total'] or 0)
        total_entradas = float(entradas_periodo['total'] or 0)

        return render(request, 'caixa.html', {
            'saldo': (total_entradas + total_compensado) - total_despesas,
            'total_entradas': total_entradas + total_compensado,
            'total_despesas': total_despesas,
            'total_cheques': total_cheques,
            'total_valor_repassado': total_repassado,
            'total_cheque_emitido': total_emitido,
            'total_valor_compensado': total_compensado
        })

    return render(request, 'caixa.html', {
        'saldo': (total_entradas + total_compensado) - total_despesas,
        'total_entradas': total_entradas + total_compensado,
        'total_despesas': total_despesas,
        'total_cheques': total_cheques,
        'total_valor_repassado': total_repassado,
        'total_cheque_emitido': total_emitido,
        'total_valor_compensado': total_compensado
    })

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def caixa_kpi(request):
    """Retorna KPIs do caixa como JSON — aceita start_date e end_date opcionais."""
    from django.db.models import Sum, Case, When, Value, IntegerField

    empresa = request.user.empresa
    start_date = request.GET.get('start_date')
    end_date   = request.GET.get('end_date')

    cheques_agg = Cheque.objects.filter(empresa=empresa).aggregate(
        total_emitido=Sum(Case(When(situacao='E', then='valor'), default=Value(0), output_field=IntegerField())),
        total_compensado=Sum(Case(When(situacao='C', then='valor'), default=Value(0), output_field=IntegerField())),
    )
    total_emitido    = float(cheques_agg['total_emitido']    or 0)
    total_compensado = float(cheques_agg['total_compensado'] or 0)

    qs_entradas = ContaReceber.objects.filter(recebido=True, empresa=empresa)
    qs_despesas = ContaPagar.objects.filter(pago=True,     empresa=empresa)

    if start_date and end_date:
        qs_entradas = qs_entradas.filter(data_recebimento__range=[start_date, end_date])
        qs_despesas = qs_despesas.filter(data_pagamento__range=[start_date, end_date])

    total_entradas = float(qs_entradas.aggregate(t=Sum('valor'))['t'] or 0) + total_compensado
    total_despesas = float(qs_despesas.aggregate(t=Sum('valor'))['t'] or 0)

    return JsonResponse({
        'total_entradas':     total_entradas,
        'total_despesas':     total_despesas,
        'total_cheque_emitido': total_emitido,
        'saldo':              total_entradas - total_despesas,
    })


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def total_despesa_categoria(request):
    from django.db.models import Sum

    # Otimizado: Uma única query com agregação por categoria
    despesas_por_categoria = ContaPagar.objects.filter(
        pago=True,
        empresa=request.user.empresa
    ).values('categoria__nome_categoria').annotate(
        total=Sum('valor')
    ).order_by('categoria__nome_categoria')

    # Converte para dicionário
    total_d_categoria = {item['categoria__nome_categoria']: float(item['total'] or 0) for item in despesas_por_categoria}

    return JsonResponse({'total_d_categoria': total_d_categoria})

@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def total_despesa_ano_atual(request):
    from django.db.models import Sum

    ano_atual = datetime.now().year
    meses_anteriores = list(range(1, 13))

    # Otimizado: Uma única query com agregação por mês
    despesas_mensais = ContaPagar.objects.filter(
        data_pagamento__year=ano_atual,
        pago=True,
        empresa=request.user.empresa
    ).values('data_pagamento__month').annotate(
        total=Sum('valor')
    ).order_by('data_pagamento__month')

    # Converte para dicionário para acesso rápido
    despesas_dict = {item['data_pagamento__month']: float(item['total'] or 0) for item in despesas_mensais}

    # Preenche lista com valores (0 para meses sem despesas)
    total_despesas = [despesas_dict.get(mes, 0) for mes in meses_anteriores]

    return JsonResponse({
        'total_despesas': total_despesas,
        'meses': meses_anteriores,
        'ano_atual': ano_atual
    })
    


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def get_available_years(request):
    """
    Retorna os anos disponíveis com base nas datas de pagamento e recebimento
    """
    from django.db.models import Min, Max
    
    # Obtém o ano mínimo e máximo das despesas
    despesas_years = ContaPagar.objects.filter(
        empresa=request.user.empresa,
        pago=True
    ).aggregate(
        min_year=Min('data_pagamento__year'),
        max_year=Max('data_pagamento__year')
    )
    
    # Obtém o ano mínimo e máximo das entradas
    entradas_years = ContaReceber.objects.filter(
        empresa=request.user.empresa,
        recebido=True
    ).aggregate(
        min_year=Min('data_recebimento__year'),
        max_year=Max('data_recebimento__year')
    )
    
    # Determina o intervalo de anos
    min_year = min(
        despesas_years['min_year'] or datetime.now().year,
        entradas_years['min_year'] or datetime.now().year
    )
    max_year = max(
        despesas_years['max_year'] or datetime.now().year,
        entradas_years['max_year'] or datetime.now().year
    )
    
    # Cria lista de anos disponíveis
    years = list(range(min_year, max_year + 1))
    years.reverse()  # Ordem decrescente (mais recente primeiro)
    
    return JsonResponse({
        'years': years,
        'current_year': datetime.now().year
    })


@login_required(login_url='/auth/login/')
@has_role_decorator(lista_permissoes_financeiro)
def saldo_anual(request):
    from django.db.models import Sum

    ano = request.GET.get('year', datetime.now().year)
    start_date = request.GET.get('start_date')
    end_date   = request.GET.get('end_date')

    try:
        ano = int(ano)
    except (ValueError, TypeError):
        ano = datetime.now().year

    meses_anteriores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    empresa = request.user.empresa

    qs_despesas = ContaPagar.objects.filter(pago=True, empresa=empresa)
    qs_entradas = ContaReceber.objects.filter(recebido=True, empresa=empresa)

    if start_date and end_date:
        qs_despesas = qs_despesas.filter(data_pagamento__range=[start_date, end_date])
        qs_entradas = qs_entradas.filter(data_recebimento__range=[start_date, end_date])
    else:
        qs_despesas = qs_despesas.filter(data_pagamento__year=ano)
        qs_entradas = qs_entradas.filter(data_recebimento__year=ano)

    despesas_dict = {
        item['data_pagamento__month']: float(item['total'] or 0)
        for item in qs_despesas.values('data_pagamento__month').annotate(total=Sum('valor'))
    }
    entradas_dict = {
        item['data_recebimento__month']: float(item['total'] or 0)
        for item in qs_entradas.values('data_recebimento__month').annotate(total=Sum('valor'))
    }

    total_despesas = [despesas_dict.get(m, 0) for m in meses_anteriores]
    total_entradas = [entradas_dict.get(m, 0) for m in meses_anteriores]
    saldo          = [entradas_dict.get(m, 0) - despesas_dict.get(m, 0) for m in meses_anteriores]

    return JsonResponse({
        'saldo':    saldo,
        'entradas': total_entradas,
        'despesas': total_despesas,
        'meses':    meses_anteriores,
        'ano':      ano,
    })


