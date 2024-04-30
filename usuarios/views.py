from django.shortcuts import render, HttpResponse
from rolepermissions.decorators import has_role_decorator
from .models import Users
from django.contrib import auth ,messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
import openpyxl

from django.core.paginator import Paginator
# Create your views here.
@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def cadastrar_vendedor(request):
    if request.method == "GET":
        return render(request, 'cadastrar_vendedor.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        print(nome, email, senha)
        #validação de email
        users = Users.objects.filter(email=email)

        if users.exists():
            #TODO: utilizar mensagens do django
            messages.error(request,'Email já cadastrado', extra_tags='danger')
            return redirect(reverse('usuarios:cadastrar_vendedor'))
        # Aqui você deve salvar os dados do vendedor no banco de dados

        users = Users.objects.create_user(username=email, password=senha, email=email, first_name=nome, cargo='V')
        users.save()
        return redirect(reverse('usuarios:vendedores'))

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def vendedores(request):
    vendedores = Users.objects.filter(cargo='V')
    paginator = Paginator(vendedores, 10)
    page_number = request.GET.get('page')
    vendedores_obj = paginator.get_page(page_number)

    return render(request, 'vendedores.html', {'vendedores': vendedores_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def editar_vendedor(request, id):
    vendedor = Users.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'cadastrar_vendedor.html', {'vendedor': vendedor})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        print(nome, email, senha)
        # Aqui você deve atualizar os dados do vendedor no banco de dados
        vendedor.first_name = nome
        vendedor.email = email
        vendedor.set_password(senha)
        vendedor.save()
        return HttpResponse("Vendedor atualizado com sucesso!")

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def excluir_vendedor(request, id):
    vendedor = Users.objects.get(id=id)
    vendedor.delete()
    return HttpResponse("Vendedor excluído com sucesso!")

@login_required(login_url='/auth/login/')
@has_role_decorator("vendedor")
def gerar_excel_vendedores(request):

    

    vendedores = Users.objects.filter(cargo='V')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Nome', 'Email'])
    for vendedor in vendedores:
        ws.append([vendedor.first_name, vendedor.email])
    wb.save('vendedores.xlsx')
    return HttpResponse("Excel gerado com sucesso!")


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, 'login.html')
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        print(email, senha)
        # Aqui você deve fazer a validação do login
        user = auth.authenticate(username=email, password=senha)
        if user is None:
            messages.error(request, 'Usuário ou senha inválidos')
            return redirect(reverse('usuarios:login'))
        
        auth.login(request, user)

        return redirect(reverse('home'))
    

def logout(request):
    auth.logout(request)
    return redirect(reverse('usuarios:login'))