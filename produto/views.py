from django.shortcuts import render,redirect
from .models import Empreendimento, Quadra, Lote
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from cliente.models import Cliente
import uuid
# Create your views here.
@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def home_produto(request):
    empreendimentos = Empreendimento.objects.all()
    return render(request, 'produto/empreendimento/home.html', {'empreendimentos': empreendimentos})

def cadastrar_empreendimento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get('descricao')
        empreendimento = Empreendimento(nome=nome, localizacao=localizacao, descricao=descricao, imagem=imagem)
        empreendimento.save()
        messages.success(request, 'Empreendimento cadastrado com sucesso!')
        return redirect(reverse('produto:home_produto'))
    return render(request, 'produto/empreendimento/cadastrar_empreendimento.html')

@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def detalhes_empreendimento(request, id):
    empreendimento = Empreendimento.objects.get(id=id)
    quadras = Quadra.objects.filter(empreendimento=id)
    return render(request, 'produto/empreendimento/detalhes_empreendimento.html', {'empreendimento': empreendimento, 'quadras': quadras})

@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def quadras(request, id):
    quadra = Quadra.objects.get(id=id)
    lotes = Lote.objects.filter(quadra_id=quadra.id)
    return render(request, 'produto/quadra/home.html', {'quadra': quadra,  'lotes': lotes})


@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def cadastrar_quadra(request, id):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get('descricao')
        metragem = request.POST.get('metragem')
        quadra = Quadra(nome=nome, empreendimento_id=id, metragem=metragem, descricao=descricao, imagem=imagem)
        quadra.save()
        messages.success(request, 'Quadra cadastrada com sucesso!')
        return redirect(reverse('produto:detalhes_empreendimento', args=[id]))
    return render(request, 'produto/quadra/cadastrar_quadra.html', {'id': id})

@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def lotes(request, id):
    lotes = Lote.objects.filter(quadra=id)
    return render(request, 'produto/lotes.html', {'lotes': lotes})

@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def cadastrar_lote(request, id_quadra):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        metragem  = request.POST.get('metragem')
        preco = request.POST.get('preco')
        status = request.POST.get('status')
        data_aquisicao = request.POST.get('data_aquisicao')
        if data_aquisicao:
        
            lote = Lote(numero=numero, metragem=metragem, preco=preco, status=status, data_aquisicao=data_aquisicao, quadra_id=id_quadra)
        else:
             lote = Lote(numero=numero, metragem=metragem, preco=preco, status=status, quadra_id=id_quadra)
        lote.save()

        messages.success(request, 'Lote cadastrado com sucesso!')
        return redirect(reverse('produto:quadras', args=[id_quadra]))
    return render(request, 'produto/lote/cadastrar_lote.html')


@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def editar_lote(request, id):
    lote = Lote.objects.get(id=id)
    if request.method == 'POST':
        lote.numero = request.POST.get('numero')
        lote.metragem = request.POST.get('metragem')
        lote.preco = request.POST.get('preco')
        lote.status = request.POST.get('status')
        lote.data_aquisicao = request.POST.get('data_aquisicao')
        lote.save()
        messages.success(request, 'Lote editado com sucesso!')
        return redirect(reverse('produto:quadras', args=[lote.quadra.id]))
    return render(request, 'produto/lote/cadastrar_lote.html'  , {'lote': lote})

    
@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def excluir_lote(request, id):
    lote = Lote.objects.get(id=id)
    lote.delete()
    messages.success(request, 'Lote deletado com sucesso!')
    return redirect(reverse('produto:quadras', args=[lote.quadra.id]))




