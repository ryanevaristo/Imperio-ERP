from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Movimentacao, Produtos, EstoqueCategoria, Notificacao
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



# Create your views here.

@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def home_estoque(request):
    produtos = Produtos.objects.all()


    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        produtos = produtos.filter(created_at__range=[start_date, end_date])

    # Verifica se o usuário tem permissão para ver os produtos
    

    #Filtra por pesquisar se o paramento estiver presente
    pesquisar = request.GET.get('pesquisar')
    if pesquisar:
        produtos = produtos.filter(produto__icontains=pesquisar)

    #paginator
    paginator = Paginator(produtos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if start_date and end_date is None:
        return render(request, 'estoque/home.html', {'produtos': produtos, 'page_obj': page_obj, 'pesquisar':pesquisar})
    

    return render(request, 'estoque/home.html', {'produtos': produtos, 'page_obj': page_obj,'start_date': start_date, 'end_date': end_date,'pesquisar':pesquisar})

def detalhes_produto(request, id):
    produto = Produtos.objects.get(id=id)
    return render(request, 'estoque/detalhes_produto.html', {'produto': produto})

@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def cadastrar_produto(request):
    cadastrar_categoria = EstoqueCategoria.objects.all()
    if request.method == 'GET':
        return render(request, 'estoque/cadastrar_editar_produto.html', {'categorias': cadastrar_categoria})
    
    elif request.method == 'POST' and request.POST.get('nome_categoria') =='':
        produto = request.POST.get('produto')
        qtd = request.POST.get('qtd')
        qtd_min = request.POST.get('qtd_min')
        custo = request.POST.get('custo')
        preco = request.POST.get('preco')
        venda = request.POST.get('venda')
        categoria = request.POST.get('categoria')
        # Aqui você deve salvar os dados do produto no banco de dados
        calculo_margem = (float(venda) - float(custo)) / float(custo) * 100
        margem = round(calculo_margem, 2)

        produtos = Produtos(
            produto=produto,
            qtd=qtd,
            qtd_min=qtd_min,
            custo=custo,
            venda=venda,
            Margem=margem,
            categoria=EstoqueCategoria.objects.get(id=categoria)
        )
        produtos.save()
        messages.success(request, 'Produto cadastrado com sucesso!')
        return redirect(reverse('estoque:home_estoque'))
    else:
        nome_categoria = request.POST.get('nome_categoria')
        if EstoqueCategoria.objects.filter(nome_categoria=nome_categoria).exists():
            messages.error(request,'Categoria já cadastrada', extra_tags='danger')
            return redirect("financeiro:cadastrar_despesas")
        
        categorias = EstoqueCategoria(nome_categoria=nome_categoria)
        categorias.save()
        print(request.path_info)
        return HttpResponseRedirect(request.path_info)
        


@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def editar_produto(request, id):
    produto = Produtos.objects.get(id=id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        qtd = request.POST.get('qtd')
        preco = request.POST.get('preco')
        descricao = request.POST.get('descricao')
        produto.nome = nome
        produto.qtd = qtd
        produto.preco = preco
        produto.descricao = descricao
        produto.save()
        messages.success(request, 'Produto editado com sucesso!')
        return redirect(reverse('estoque:home_estoque'))
    return render(request, 'estoque/cadastrar_editar_produto.html', {'produto': produto})


@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def deletar_produto(request, id):
    produto = Produtos.objects.get(id=id)
    produto.delete()
    messages.success(request, 'Produto deletado com sucesso!')
    return redirect(reverse('estoque:home_estoque'))


@login_required(login_url='/auth/login/')
@has_role_decorator(["gerente", "administrador"])
def cadastrar_categorias(request):
    if request.method == "GET":
        cadastrar_categorias = EstoqueCategoria.objects.all()
        return render(request, 'cadastrar_categoria_estoque.html', {'categorias': cadastrar_categorias})
    elif request.method == "POST":
        descricao = request.POST.get('nome_categoria')
        if EstoqueCategoria.objects.filter(descricao=descricao).exists():
            messages.error(request, 'Categoria já existe!', extra_tags='danger')
            return redirect(reverse('estoque:cadastrar_categorias'))
        print(descricao)
        # Aqui você deve salvar os dados da categoria no banco de dados
        categoria = EstoqueCategoria(descricao=descricao)
        categoria.save()
        return redirect('/estoque/')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Produtos, Movimentacao
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator

@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def movimentacao(request, produto_id):  # Certifique-se de que está recebendo produto_id
    if request.method == 'POST':
        qtd = request.POST.get('qtd')
        tipo = request.POST.get('tipo_movimentacao')
        motivo = request.POST.get('motivo')

        try:
            produto_obj = Produtos.objects.get(id=produto_id)  # Buscando o produto correto
        except Produtos.DoesNotExist:
            messages.error(request, 'Produto não encontrado!', extra_tags='danger')
            return redirect(reverse('estoque:home_estoque'))

        # Atualiza a quantidade do produto no estoque
        if tipo == 'Entrada':
            produto_obj.qtd += int(qtd)
        elif tipo == 'Saida':
            produto_obj.qtd -= int(qtd)
        elif tipo == 'Devolucao':
            produto_obj.qtd += int(qtd)

        # Verifica se a quantidade não fica negativa
        if produto_obj.qtd < 0:
            messages.error(request, 'Quantidade não pode ser negativa!', extra_tags='danger')
            return redirect(reverse('estoque:home_estoque'))

        # Salva a movimentação no banco de dados
        movimentacao = Movimentacao(
            produto=produto_obj,
            qtd=qtd,
            tipo=tipo,
            motivo=motivo
        )
        movimentacao.save()

        # Atualiza a quantidade do produto no banco de dados
        produto_obj.save()

        if produto_obj.qtd < produto_obj.qtd_min:
            Notificacao.objects.create(
                produto=produto_obj,
                mensagem=f'O produto {produto_obj.produto} está abaixo do estoque mínimo!'
            )
            messages.success(request, 'Movimentação realizada com sucesso!', extra_tags='success')
            return redirect(reverse('estoque:home_estoque'))    
        

        # Redireciona para a página de movimentação com uma mensagem de sucesso
        messages.success(request, 'Movimentação realizada com sucesso!')
        return redirect(reverse('estoque:home_estoque'))

    return redirect(reverse('estoque:home_estoque'))

@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def relatorio_estoque(request):
    if request.method == 'POST':
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        tipo = request.POST.get('tipo')
        produto_id = request.POST.get('produto')
        produto = request.POST.get('produto')
        if produto_id:
            movimentacoes = Movimentacao.objects.filter(produto__id=produto_id, created_at__range=[data_inicial, data_final])
        else:
            movimentacoes = Movimentacao.objects.filter(created_at__range=[data_inicial, data_final])
        if tipo:
            movimentacoes = movimentacoes.filter(tipo=tipo)
            return render(request, 'estoque/relatorio_estoque.html', {'movimentacoes':
                                                                      movimentacoes})
    else:
        movimentacoes = Movimentacao.objects.all()
    produtos = Produtos.objects.all()
    return render(request, 'estoque/relatorio_estoque.html', {'movimentacoes': movimentacoes, 'produtos': produtos})


@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def listar_notificacoes(request):
    notificacoes = Notificacao.objects.filter(visualizado=False).order_by('-data_criacao')
    return render(request, 'estoque/notificacoes.html', {'notificacoes': notificacoes,'notificacoes_count': notificacoes.count()})



@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def marca_vizualizado(request, id):
    try:
        notificacao = Notificacao.objects.get(id=id)
        notificacao.visualizado = True
        notificacao.save()
        messages.success(request, 'Notificação marcada como visualizada!')
    except Notificacao.DoesNotExist:
        messages.error(request, 'Notificação não encontrada!', extra_tags='danger')
    return redirect(request.META.get('HTTP_REFERER', 'estoque:notificacoes'))

