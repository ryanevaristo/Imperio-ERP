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
    # Otimizado: Usa select_related para empresa e only() para campos necessários
    usuarios = Users.objects.select_related('empresa').filter(
        cargo="G",
        empresa=request.user.empresa
    ).only(
        'first_name', 'email', 'telefone', 'username', 'empresa__nome'
    ).order_by('first_name')
    
    if not usuarios.exists():
        messages.error(request, 'Não existem vendedores cadastrados', extra_tags='danger')
        return redirect(reverse('usuarios:Usuarios'))
    
    # Cria lista de dicionários diretamente sem queries adicionais
    usuarios_data = []
    for usuario in usuarios:
        usuarios_data.append({
            'Nome': usuario.first_name,
            'Email': usuario.email,
            'Username': usuario.username,
            'Telefone': usuario.telefone or '',
            'Empresa': usuario.empresa.nome if usuario.empresa else ''
        })
    
    df = pd.DataFrame(usuarios_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Usuarios', index=False)
    
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
        
        # Primeiro, tenta autenticar o usuário
        user = auth.authenticate(username=email, password=senha)
        
        if user is None:
            # Verifica se o usuário existe mas a mensalidade está vencida
            try:
                from .models import Users
                user_check = Users.objects.select_related('empresa').get(username=email)
                
                # Verifica a senha manualmente
                if user_check.check_password(senha):
                    # Senha correta, mas autenticação falhou - provavelmente mensalidade vencida
                    if user_check.empresa and not user_check.empresa.pode_acessar_sistema():
                        messages.error(
                            request, 
                            'Sua mensalidade está vencida. Entre em contato com o suporte para renovar o acesso ao sistema.',
                            extra_tags='danger'
                        )
                        return redirect(reverse('usuarios:login'))
            except Users.DoesNotExist:
                pass
            
            # Se chegou aqui, é realmente usuário ou senha inválidos
            messages.error(request, 'Usuário ou senha inválidos', extra_tags='danger')
            return redirect(reverse('usuarios:login'))
        
        # Verifica novamente a mensalidade antes de fazer login (segurança extra)
        if hasattr(user, 'empresa') and user.empresa:
            if not user.empresa.pode_acessar_sistema():
                messages.error(
                    request,
                    'Sua mensalidade está vencida. Entre em contato com o suporte para renovar o acesso ao sistema.',
                    extra_tags='danger'
                )
                return redirect(reverse('usuarios:login'))
        
        auth.login(request, user)
        return redirect(reverse('home'))
    

def logout(request):
    auth.logout(request)
    return redirect(reverse('usuarios:login'))


