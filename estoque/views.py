from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Produtos, Categoria
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def home_estoque(request):
    produtos = Produtos.objects.all()
    return render(request, 'estoque/home.html', {'produtos': produtos})

def detalhes_produto(request, id):
    produto = Produtos.objects.get(id=id)
    return render(request, 'estoque/detalhes_produto.html', {'produto': produto})

@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def cadastrar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        qtd = request.POST.get('qtd')
        preco = request.POST.get('preco')
        descricao = request.POST.get('descricao')
        produto = Produtos(nome=nome, qtd=qtd, preco=preco, descricao=descricao)
        produto.save()
        messages.success(request, 'Produto cadastrado com sucesso!')
        return redirect(reverse('estoque:home_estoque'))
    return render(request, 'estoque/cadastrar_produto.html')

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
    return render(request, 'estoque/editar_produto.html', {'produto': produto})


@login_required(login_url='/login/')
@has_role_decorator(["Administrador", "Gerente"])
def deletar_produto(request, id):
    produto = Produtos.objects.get(id=id)
    produto.delete()
    messages.success(request, 'Produto deletado com sucesso!')
    return redirect(reverse('estoque:home_estoque'))

