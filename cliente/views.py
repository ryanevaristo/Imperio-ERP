from django.shortcuts import render, redirect
from .models import Cliente
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator


# Create your views here.

@login_required(login_url='/login/')
@has_role_decorator('vendedor')
def listar_clientes(request):
    clientes = Cliente.objects.all()
    paginator = Paginator(clientes, 10)
    page = request.GET.get('page')
    clientes = paginator.get_page(page)
    
    if request.GET.get("pesquisar"):
        pesquisar = request.GET.get("pesquisar")
        clientes = Cliente.objects.filter(nome_completo__icontains=pesquisar)
        paginator = Paginator(clientes, 10)
        page = request.GET.get('page')
        clientes = paginator.get_page(page)
        


    return render(request, 'clientes.html', {'clientes_obj': clientes})

@login_required(login_url='/login/')
def cadastrar_clientes(request):
    if request.method == 'POST':
        nome_completo = request.POST['nome_completo']
        email = request.POST['email']
        telefone = request.POST['telefone']
        cpf_cnpj = request.POST['cpf_cnpj']
        endereco = request.POST['endereco']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        cep = request.POST['cep']
        cliente = Cliente(nome_completo=nome_completo, email=email, telefone=telefone, cpf_cnpj=cpf_cnpj, endereco=endereco, cidade=cidade, estado=estado, cep=cep)
        cliente.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('/clientes/')
    return render(request, 'cadastrar_clientes.html')

@login_required(login_url='/login/')
def editar_clientes(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        cliente.nome_completo = request.POST['nome_completo']
        cliente.email = request.POST['email']
        cliente.telefone = request.POST['telefone']
        cliente.cpf_cnpj = request.POST['cpf_cnpj']
        cliente.endereco = request.POST['endereco']
        cliente.cidade = request.POST['cidade']
        cliente.estado = request.POST['estado']
        cliente.cep = request.POST['cep']
        cliente.save()
        messages.success(request, 'Cliente editado com sucesso!')
        return redirect('/clientes/')
    return render(request, 'cadastrar_clientes.html', {'cliente': cliente})

@login_required(login_url='/login/')
def deletar_clientes(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    messages.success(request, 'Cliente deletado com sucesso!')
    return redirect('/clientes/')

