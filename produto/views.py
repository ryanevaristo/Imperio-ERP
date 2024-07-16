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
        empreendimento = Empreendimento(nome=nome, localizacao=localizacao, foto=foto)
        empreendimento.save()
        messages.success(request, 'Empreendimento cadastrado com sucesso!')
        return redirect(reverse('produto:home_produto'))
    return render(request, 'produto/empreendimento/cadastrar_empreendimento.html')


@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def quadras(request, id):
    quadras = Quadra.objects.filter(empreendimento=id)
    return render(request, 'produto/quadras.html', {'quadras': quadras})

@login_required(login_url='/login/')
@has_role_decorator("Administrador")
def lotes(request, id):
    lotes = Lote.objects.filter(quadra=id)
    return render(request, 'produto/lotes.html', {'lotes': lotes})

