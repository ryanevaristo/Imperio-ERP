from django.shortcuts import render, HttpResponse
from rolepermissions.decorators import has_role_decorator
from django.core.exceptions import PermissionDenied
from .models import Users
from django.contrib import auth ,messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
import openpyxl
import pandas as pd
import io

from django.core.paginator import Paginator
# Create your views here.
@login_required(login_url='/auth/login/')
@has_role_decorator("Administrador")
def cadastrar_usuario(request):
    if request.method == "GET":
        return render(request, 'cadastrar_usuario.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')
        cargo = request.POST.get('cargo')

        print(nome, email, senha)
        #validação de email
        users = Users.objects.filter(email=email)

        if users.exists():
            #TODO: utilizar mensagens do django
            messages.error(request,'Email já cadastrado', extra_tags='danger')
            return redirect(reverse('usuarios:cadastrar_usuario'))

        users = Users.objects.create_user(username=email, password=senha, email=email, first_name=nome, cargo=cargo, telefone=telefone, empresa=request.user.empresa)
        users.save()
        return redirect(reverse('usuarios:Usuarios'))

@login_required(login_url='/auth/login/')
@has_role_decorator("Administrador")
def Usuarios(request):
    usuarios = Users.objects.all()
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios_obj = paginator.get_page(page_number)

    if request.GET.get("pesquisar"):
        pesquisar = request.GET.get("pesquisar")
        usuarios_obj = Users.objects.filter(first_name__icontains=pesquisar)
        paginator = Paginator(usuarios_obj, 10)
        page_number = request.GET.get('page')
        usuarios_obj = paginator.get_page(page_number)
        

    return render(request, 'Usuarios.html', {'usuarios_obj': usuarios_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("Administrador")
def editar_usuario(request, id):
    usuario = Users.objects.get(id=id)
    if request.method == "GET":
        return render(request, 'cadastrar_usuario.html', {'usuario': usuario})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')
        cargo = request.POST.get('cargo')
        print(nome, email, senha)
        # Aqui você deve atualizar os dados do usuario no banco de dados
        usuario.first_name = nome
        usuario.email = email
        usuario.telefone = telefone
        usuario.cargo = cargo
        usuario.set_password(senha)
        usuario.save()
        messages.success(request, 'usuario atualizado com sucesso!')
        return redirect(reverse('usuarios:Usuarios'))

@login_required(login_url='/auth/login/')
@has_role_decorator("Administrador")
def excluir_usuario(request, id):
    vendedor = Users.objects.get(id=id)
    vendedor.delete()
    return redirect(reverse('usuarios:Usuarios'))

@login_required(login_url='/auth/login/')
@has_role_decorator("Administrador")
def exportar_Usuarios_xlsx(request):
    Usuarios = Users.objects.filter(cargo="G")
    if Usuarios.count() == 0:
        messages.error(request, 'Não existem vendedores cadastrados', extra_tags='danger')
        return redirect(reverse('usuarios:Usuarios'))
    df = pd.DataFrame(list(Usuarios.values()))
    df = df.drop(columns=['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'cargo', 'id'])
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Usuarios')
    writer.close()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Usuarios.xlsx'
    return response
     

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
            messages.error(request, 'Usuário ou senha inválidos', extra_tags='danger')
            return redirect(reverse('usuarios:login'))
        
        auth.login(request, user)

        return redirect(reverse('home'))
    

def logout(request):
    auth.logout(request)
    return redirect(reverse('usuarios:login'))


