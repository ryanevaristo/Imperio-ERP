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
    # Otimizado: Usa select_related para empresa e filtra eficientemente
    clientes = Cliente.objects.select_related('empresa').filter(empresa=request.user.empresa).order_by('-data_cadastro')

    if request.GET.get("pesquisar"):
        pesquisar = request.GET.get("pesquisar")
        clientes = clientes.filter(
            nome_completo__icontains=pesquisar
        ) | clientes.filter(
            cpf_cnpj__icontains=pesquisar
        ) | clientes.filter(
            email__icontains=pesquisar
        )

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
            cliente = form.save(commit=False)
            cliente.empresa = request.user.empresa
            cliente.save()  # Salve o cliente no banco de dados
            messages.success(request, 'Cliente cadastrado com sucesso!')
            
            return redirect('/clientes/')  # Redirecione para a lista de clientes
        else:
            messages.error(request, f"Este Cpf ou Cnpj já existe", extra_tags='warning')
    else:
        form = ClienteForm()

    return render(request, 'cadastrar_clientes.html', {'form': form})

@login_required(login_url='/login/')
def editar_clientes(request, id):
    # Otimizado: Usa select_related para empresa
    cliente = Cliente.objects.select_related('empresa').get(id=id, empresa=request.user.empresa)
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
    cliente = Cliente.objects.get(id=id, empresa=request.user.empresa)
    cliente.delete()
    messages.success(request, 'Cliente deletado com sucesso!')
    return redirect('/clientes/')

@login_required(login_url='/login/')
def exportar_clientes_xlsx(request):
    # Otimizado: Usa only() para buscar apenas campos necessários
    clientes = Cliente.objects.filter(empresa=request.user.empresa).only(
        'nome_completo', 'cpf_cnpj', 'email', 'telefone', 'cep', 
        'cidade', 'estado', 'endereco', 'data_cadastro'
    )
    df = pd.DataFrame(list(clientes.values(
        'nome_completo', 'cpf_cnpj', 'email', 'telefone', 'cep', 
        'cidade', 'estado', 'endereco', 'data_cadastro'
    )))
    
    if not df.empty:
        df['data_cadastro'] = pd.to_datetime(df['data_cadastro']).dt.strftime('%d/%m/%Y %H:%M:%S')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Clientes', index=False)
    
    output.seek(0)
    response = HttpResponse(
        output, 
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=clientes.xlsx'
    return response
     

@login_required(login_url='/login/')
def exportar_clientes_pdf(request):
    # Otimizado: Usa only() e renderiza template HTML customizado
    clientes = Cliente.objects.filter(empresa=request.user.empresa).only(
        'nome_completo', 'cpf_cnpj', 'email', 'telefone', 'cidade', 
        'estado', 'data_cadastro'
    ).order_by('nome_completo')
    
    html_string = render(request, 'clientes_pdf.html', {
        'clientes': clientes,
        'empresa': request.user.empresa
    }).content.decode('utf-8')
    
    pdf = pdfkit.from_string(html_string, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=clientes.pdf'
    
    return response


