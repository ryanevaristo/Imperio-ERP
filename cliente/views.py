from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Cliente
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from rolepermissions.decorators import has_role_decorator
from .forms import ClienteForm
import pandas as pd
import io
import pdfkit



# Create your views here.

def clear_messages(request):
    storage = messages.get_messages(request)
    storage.used = True

@login_required(login_url='/login/')
@has_role_decorator('gerente')
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
@has_role_decorator('gerente')
def cadastrar_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)  # Use o formulário de Cliente (se você tiver um)
        if form.is_valid():
            form.save()  # Salve o cliente no banco de dados
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('/clientes/')  # Redirecione para a lista de clientes
        else:
            messages.error(request, f'{form.errors['telefone']}',extra_tags='warning')
    else:
        form = ClienteForm()  # Crie um novo formulário em caso de GET

    return render(request, 'cadastrar_clientes.html', {'form': form})

@login_required(login_url='/login/')
def editar_clientes(request, id):
    cliente = Cliente.objects.get(id=id)
    clear_messages(request)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente editado com sucesso!')
            return redirect('/clientes/')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cadastrar_clientes.html', {'cliente': form})

@login_required(login_url='/login/')
def deletar_clientes(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    messages.success(request, 'Cliente deletado com sucesso!')
    return redirect('/clientes/')

@login_required(login_url='/login/')
def exportar_clientes_xlsx(request):
    clientes = Cliente.objects.all()
    df = pd.DataFrame(list(clientes.values()))
    df['data_cadastro'] = df['data_cadastro'].dt.strftime('%d/%m/%Y %H:%M:%S')
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Clientes' ,index=False)
    writer.close()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=clientes.xlsx'
    return response
     

@login_required(login_url='/login/')
def exportar_clientes_pdf(request):
    clientes = Cliente.objects.all()
    df = pd.DataFrame(list(clientes.values()))
    df['data_cadastro'] = df['data_cadastro'].dt.strftime('%d/%m/%Y %H:%M:%S')
    html_string = df.to_html()
    pdf = pdfkit.from_string(html_string, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=clientes.pdf'


    return response


