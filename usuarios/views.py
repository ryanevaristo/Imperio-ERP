from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import assign_role
from django.core.exceptions import PermissionDenied
from .models import Users
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from django.core.mail import send_mail
from datetime import date, timedelta
import logging
import openpyxl
import pandas as pd
import io

from core.models import Empresa
from django.core.paginator import Paginator
from django.conf import settings

logger = logging.getLogger(__name__)
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
    usuarios = Users.objects.filter(empresa=request.user.empresa)

    if request.GET.get("pesquisar"):
        pesquisar = request.GET.get("pesquisar")
        usuarios = usuarios.filter(first_name__icontains=pesquisar)

    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios_obj = paginator.get_page(page_number)
        

    return render(request, 'Usuarios.html', {'usuarios_obj': usuarios_obj})

@login_required(login_url='/auth/login/')
@has_role_decorator("Administrador")
def editar_usuario(request, id):
    usuario = get_object_or_404(Users, id=id, empresa=request.user.empresa)
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
    vendedor = get_object_or_404(Users, id=id, empresa=request.user.empresa)
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
     

def _get_client_ip(request):
    """Retorna o IP real do cliente mesmo atrás de proxy/nginx."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, 'login.html')

    elif request.method == "POST":
        from django.core.cache import cache

        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')
        ip    = _get_client_ip(request)

        # ── Brute-force: bloqueia após 5 tentativas por IP (1 hora) ──────────
        cache_key  = f'login_fail_{ip}'
        fail_count = cache.get(cache_key, 0)
        LOCKOUT_LIMIT   = 5
        LOCKOUT_SECONDS = 3600  # 1 hora

        if fail_count >= LOCKOUT_LIMIT:
            minutes = LOCKOUT_SECONDS // 60
            messages.error(
                request,
                f'Muitas tentativas de login. Seu acesso está bloqueado por {minutes} minutos.',
                extra_tags='danger',
            )
            return redirect(reverse('usuarios:login'))
        # ─────────────────────────────────────────────────────────────────────

        # Tenta autenticar o usuário
        user = auth.authenticate(request, username=email, password=senha)

        if user is None:
            # Incrementa contador de falhas
            cache.set(cache_key, fail_count + 1, LOCKOUT_SECONDS)

            # Verifica se existe mas mensalidade vencida
            try:
                user_check = Users.objects.select_related('empresa').get(username=email)
                if user_check.check_password(senha):
                    if user_check.empresa and not user_check.empresa.pode_acessar_sistema():
                        messages.error(
                            request,
                            'Sua mensalidade está vencida. Entre em contato com o suporte para renovar o acesso ao sistema.',
                            extra_tags='danger',
                        )
                        return redirect(reverse('usuarios:login'))
            except Users.DoesNotExist:
                pass

            remaining = LOCKOUT_LIMIT - (fail_count + 1)
            if remaining > 0:
                messages.error(
                    request,
                    f'Usuário ou senha inválidos. {remaining} tentativa{"s" if remaining != 1 else ""} restante{"s" if remaining != 1 else ""} antes do bloqueio.',
                    extra_tags='danger',
                )
            else:
                messages.error(
                    request,
                    'Acesso bloqueado por 1 hora devido a múltiplas tentativas de login.',
                    extra_tags='danger',
                )
            return redirect(reverse('usuarios:login'))

        # Verifica mensalidade antes de logar
        if hasattr(user, 'empresa') and user.empresa:
            if not user.empresa.pode_acessar_sistema():
                messages.error(
                    request,
                    'Sua mensalidade está vencida. Entre em contato com o suporte para renovar o acesso ao sistema.',
                    extra_tags='danger',
                )
                return redirect(reverse('usuarios:login'))

        # Login bem-sucedido — reseta contador de falhas
        cache.delete(cache_key)
        auth.login(request, user)
        return redirect(reverse('home'))
    

def logout(request):
    auth.logout(request)
    return redirect(reverse('usuarios:login'))


def cadastro(request):
    """Cadastro self-service — cria Empresa + usuário admin com período de teste."""
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == 'GET':
        return render(request, 'cadastro.html')

    # POST — valida e cria conta
    nome_completo = request.POST.get('nome_completo', '').strip()
    email        = request.POST.get('email', '').strip().lower()
    senha        = request.POST.get('senha', '')
    senha_confirm = request.POST.get('senha_confirm', '')
    nome_empresa = request.POST.get('nome_empresa', '').strip()
    cnpj         = request.POST.get('cnpj', '').strip()
    telefone     = request.POST.get('telefone', '').strip()

    ctx = {'form_data': request.POST}

    # — Validações —
    if not all([nome_completo, email, senha, nome_empresa]):
        messages.error(request, 'Preencha todos os campos obrigatórios.', extra_tags='danger')
        return render(request, 'cadastro.html', ctx)

    if senha != senha_confirm:
        messages.error(request, 'As senhas não conferem.', extra_tags='danger')
        return render(request, 'cadastro.html', ctx)

    if len(senha) < 6:
        messages.error(request, 'A senha deve ter pelo menos 6 caracteres.', extra_tags='danger')
        return render(request, 'cadastro.html', ctx)

    if Users.objects.filter(email=email).exists():
        messages.error(request, 'Este e-mail já está cadastrado.', extra_tags='danger')
        return render(request, 'cadastro.html', ctx)

    if Empresa.objects.filter(nome__iexact=nome_empresa).exists():
        messages.error(request, 'Já existe uma empresa com este nome. Use outro nome.', extra_tags='danger')
        return render(request, 'cadastro.html', ctx)

    # — Cria Empresa + Usuário atomicamente —
    try:
        with transaction.atomic():
            trial_end = date.today() + timedelta(days=7)
            empresa = Empresa.objects.create(
                nome=nome_empresa,
                cnpj=cnpj or None,
                email=email,
                telefone=telefone or None,
                mensalidade_ativa=True,
                data_vencimento_mensalidade=trial_end,
            )
            user = Users.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome_completo,
                cargo='A',
                telefone=telefone or None,
                empresa=empresa,
            )
            # Atribui papel de Administrador usando a classe diretamente
            try:
                from imperio.roles import Administrador
                assign_role(user, Administrador)
            except Exception as role_err:
                logger.warning(f'assign_role falhou: {role_err}')
                # Não bloqueia — o usuário é criado mesmo sem o role
    except Exception as e:
        logger.error(f'Erro ao criar conta: {e}', exc_info=True)
        err_msg = str(e) if settings.DEBUG else 'Erro ao criar conta. Tente novamente mais tarde.'
        messages.error(request, err_msg, extra_tags='danger')
        return render(request, 'cadastro.html', ctx)

    # — Envia e-mail de boas-vindas (silencioso em caso de falha) —
    try:
        send_mail(
            subject='Bem-vindo ao Alicerce! 🏗️',
            message=(
                f'Olá {nome_completo},\n\n'
                f'Sua conta no Alicerce foi criada com sucesso!\n\n'
                f'Empresa: {nome_empresa}\n'
                f'E-mail: {email}\n\n'
                f'Você tem 7 dias de avaliação gratuita. Aproveite!\n\n'
                f'Acesse agora: https://alicerce.pulsarianalytics.com.br/auth/login/\n\n'
                f'Qualquer dúvida, fale com nosso suporte.\n\n'
                f'Equipe Alicerce — Pulsari Analytics'
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )
    except Exception:
        pass

    messages.success(
        request,
        f'Conta criada com sucesso! Você tem 7 dias de avaliação gratuita. Faça login para começar.',
    )
    return redirect(reverse('usuarios:login'))


