from django.shortcuts import render,redirect
from .models import Empreendimento, Quadra, Lote
from rolepermissions.decorators import has_role_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


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
        foto = request.FILES.get('foto')
        descricao = request.POST.get('descricao')
        empreendimento = Empreendimento(nome=nome, localizacao=localizacao, descricao=descricao, foto=foto)
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
    return render(request, 'produto/quadra/home.html', {'quadra': quadra})

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
def cadastrar_lote(request, id):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        valor = request.POST.get('valor')
        lote = Lote(numero=numero, valor=valor, quadra_id=id)
        lote.save()
        messages.success(request, 'Lote cadastrado com sucesso!')
        return redirect(reverse('produto:lotes', args=[id]))
    return render(request, 'produto/cadastrar_lote.html', {'id': id})

